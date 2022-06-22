"""
This module defines the AgentManager class
"""
from cmath import e
from enum import auto
import string
from typing import Dict, Optional
import docker
from docker.models.containers import Container
from docker.client import DockerClient
from docker.models.images import Image
from .agent import Agent
import requests
import time
import pika


def append_if(entry: str, original: list, test: bool) -> list:
    """
    Appends to original a new element entry, if test is True
    """
    if test is not None:
        original.append(entry)
    return original


class AgentBlueprint:
    """
    Agent Blueprint is used to generate new Agents
    """

    def __init__(self, image: Image, name: str):
        self.__name = name
        self.__image = image
        self.__envs = {}

    @property
    def name(self):
        """
        Retrieves the name of the blueprint
        """
        return self.__name

    @property
    def image(self):
        """
        Retrieves the docker image associated with this blueprint
        """
        return self.__image

    @property
    def environment_variables(self):
        """
        Retrieves the blueprint environment variables
        """
        return self.__envs

    def add_environment_variable(self, name: str, value: str):
        """
        Add environment variable to the blueprint
        """
        self.__envs[name] = value


class AgentCache:
    """
    Agent Cache Management
    """

    def __init__(self):
        self.__cache = {}

    def add(self, agent: Agent) -> str:
        """
        Add agent to the cache.

        returns the cache name Entry
        """
        if self.has(agent.name):
            return
        self.__cache[agent.name] = agent

        return agent.name

    def get(self, name: str) -> Optional[Agent]:
        """
        Retrieves the agent by name
        """
        if not self.has(name):
            return None
        return self.__cache[name]

    def has(self, name: str) -> bool:
        """
        Tests if the cache has agent with 'name'
        """
        return name in self.__cache

    def erase(self, name: str) -> None:
        """
        Remove entry with name
        """
        if not self.has(name):
            return

        self.__cache.pop(name)


class MessageBrooker:

    def __init__(self, docker_client) -> None:

        # 1. Create new Message Brooker container
        socialcraft_brookers = docker_client.containers.list(
            filters={"name": "socialcraft-brooker"}, all=True
        )

        if len(socialcraft_brookers) > 0:
            for brooker in socialcraft_brookers:
                brooker.remove(force=True)

        docker_client.containers.run(
            "rabbitmq:management",
            detach=True,
            ports={"5672/tcp": 5672, "15672/tcp": 15672},
            name="socialcraft-brooker",
            environment={
                "RABBITMQ_DEFAULT_USER": "socialcraft",
                "RABBITMQ_DEFAULT_PASS": "redstone",
            },
        )

        # 2. Wait for the Message Brooker to start
        while True:
            try:
                requests.get(f"http://host.docker.internal:15672/api")
                break
            except requests.exceptions.ConnectionError as e:
                time.sleep(3)

        # 3. Setup queue for state changes
        credentials = pika.PlainCredentials("socialcraft", "redstone")
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost", credentials=credentials)
        )
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(exchange="agent_state",exchange_type="direct")


    def add_agent(self, name):

        res = requests.put(
            f"http://host.docker.internal:15672/api/users/{name}",
            json={"password": name, "tags": "administrator"},
            auth=("socialcraft", "redstone"),
        )

        res = requests.put(
            f"http://host.docker.internal:15672/api/permissions/%2f/{name}",
            json={"configure": ".*", "write": ".*", "read": ".*"},
            auth=("socialcraft", "redstone"),
        )

        result = self.__channel.queue_declare(queue=name,auto_delete=False)
        self.__channel.queue_bind(exchange='agent_state', queue=name, routing_key=name)


    def set_agent_variable(self, name:string, variable: string, value: object) -> None:
        self.__channel.basic_publish(exchange='agent_state', routing_key=name, body=f"{variable}:=={value}")
       
        

class AgentManager:
    """
    The AgentManager class supervises the deployment of agents
    """

    def __init__(
        self,
        docker_url=None,
        minecraft_host=None,
        minecraft_username=None,
        minecraft_password=None,
        minecraft_port=None,
        minecraft_version=None,
        minecraft_auth=None,
    ):
        self.__cache = AgentCache()

        if docker_url is not None:
            self.__docker_client = docker.DockerClient(base_url=docker_url)
        else:
            self.__docker_client = docker.from_env()

        self.__minecraft_config = {
            "host": minecraft_host or "localhost",
            "port": minecraft_port or "25565",
            "version": minecraft_version,
            "auth": minecraft_auth,
            "username": minecraft_username,
            "password": minecraft_password,
        }

        self.__message_broker : MessageBrooker = MessageBrooker(self.__docker_client)

    def __get_docker_client(self) -> Optional[DockerClient]:
        return self.__docker_client

    def __get_docker_container(self, name: str) -> Optional[Container]:
        try:
            return self.__get_docker_client().containers.get(name)
        except docker.errors.NotFound:
            return None

    def get_all_agents(self) -> list[Agent]:
        """
        List all the agents available
        """
        agent_containers = self.__get_docker_client().containers.list(
            all=True, filters={"label": ["socialcraft_agent"]}
        )

        agents = []

        for agent_container in agent_containers:
            if self.__cache.has(agent_container.name):
                agents.append(self.__cache.get(agent_container.name))
            else:
                agent = Agent(agent_container, self)
                self.__cache.add(agent)
                agents.append(agent)

        return agents

    def create_agent(self, name: str, blueprint: AgentBlueprint, custom_envs: Dict = {}) -> Optional[Agent]:
        """
        Creates a new agent based on a previously created prototype
        """
        container = self.__get_docker_container(name)

        if container is not None:
            return None

        # when agent does not exist and cache has an entry for it, clean cache
        if self.__cache.has(name):
            self.__cache.erase(name)

        container_envs = {
            "AGENT_NAME": name,
            "RABBITMQ_HOST": "host.docker.internal",
            "RABBITMQ_PORT": "5672",
            "RABBITMQ_VIRTUAL_HOST": "/"
        }

        self.__message_broker.add_agent(name)
        self.__message_broker.set_agent_variable(name, "MINECRAFT_HOST", self.__minecraft_config["host"])
        self.__message_broker.set_agent_variable(name, "MINECRAFT_USERNAME", self.__minecraft_config["username"])
        self.__message_broker.set_agent_variable(name, "MINECRAFT_PASSWORD", self.__minecraft_config["password"])
        self.__message_broker.set_agent_variable(name, "MINECRAFT_PORT", self.__minecraft_config["port"])
        self.__message_broker.set_agent_variable(name, "MINECRAFT_VERSION", self.__minecraft_config["version"])
        self.__message_broker.set_agent_variable(name, "MINECRAFT_AUTH", self.__minecraft_config["auth"])

        agent_container = self.__get_docker_client().containers.create(
            blueprint.image,
            name=name,
            detach=True,
            environment=container_envs,
            network="bridge",
        )

        agent = Agent(agent_container, self)
        self.__cache.add(agent)
        return agent

    def kill_agent(self, name: str) -> None:
        """
        Permanentely kills an agent and destroys all associated data
        """
        # UPDATE CACHE
        #   when agent should be killed and cache has an entry for it,
        #   clean cache

        if self.__cache.has(name):
            self.__cache.erase(name)

        container = self.__get_docker_container(name)

        if container is None:
            return

        container.remove(force=True)

    def deploy_agent(self, name: str) -> None:
        """
        Deploys a previously created agent to the Minecraft Server
        """

        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it,
            #   clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it,
        #   add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container, self))

        container.start()

    def withdraw_agent(self, name: str) -> None:
        """
        Withdraws a previously deployed agent from the Minecraft Server
        """
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it,
            #   clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it,
        #   add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container, self))

        container.stop()

    def pause_agent(self, name: str) -> None:
        """
        Pauses a previously deployed agent execution
        """
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it,
            #   clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it,
        #   add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container, self))

        container.pause()

    def resume_agent(self, name: str) -> None:
        """
        Resumes a previously paused agent
        """
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it,
            #   clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it,
        #   add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container, self))

        container.unpause()

    def get_agent(self, name: str) -> Optional[Agent]:
        """
        Retrieves the agent with 'name'
        """
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it,
            #   clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            return None

        agent = Agent(container, self)

        # UPDATE CACHE
        #   when container exists but cache has no entry for it,
        #   add it to cache
        if not self.__cache.has(name):
            self.__cache.add(agent)

        return agent

    def generate_blueprint(self, name: str, agent_source_path: str) -> AgentBlueprint:
        """
        Create a new blueprint for agents based on agent_source_path
        """
        image = self.__get_docker_client().images.build(tag=name, path=agent_source_path, rm=True)
        blueprint = AgentBlueprint(image[0], name)

        return blueprint

    def set_agent_variable(self, name: str, variable_name:str, variable_value: str) -> None:
        """
        Sets the agent variable
        """
        
        self.__message_broker.set_agent_variable(name, variable_name,variable_value)