"""
This module defines the AgentManager class
"""
from typing import Optional
import docker
from docker.models.containers import Container
from docker.client import DockerClient
from docker.models.images import Image
from .agent import Agent


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
    def __init__(self, image: Image):
        self.__image = image
        self.__envs = {}

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


class AgentManager:
    """
    The AgentManager class supervises the deployment of agents
    """
    def __init__(self,
                 docker_url=None,
                 minecraft_host=None,
                 minecraft_username=None,
                 minecraft_password=None,
                 minecraft_port=None,
                 minecraft_version=None,
                 minecraft_auth=None):
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
            all=True, filters={"label": ["socialcraft_agent"]})

        agents = []

        for agent_container in agent_containers:
            if self.__cache.has(agent_container.name):
                agents.append(self.__cache.get(agent_container.name))
            else:
                agent = Agent(agent_container, self)
                self.__cache.add(agent)
                agents.append(agent)

        return agents

    def create_agent(self, name: str,
                     blueprint: AgentBlueprint) -> Optional[Agent]:
        """
        Creates a new agent based on a previously created prototype
        """
        container = self.__get_docker_container(name)

        if container is not None:
            print(f"Agent with name '{name}' already exists.")
            return None

        # when agent does not exist and cache has an entry for it, clean cache
        if self.__cache.has(name):
            self.__cache.erase(name)

        container_envs = {}

        if self.__minecraft_config['host'] is not None:
            container_envs["MINECRAFT_HOST"] = self.__minecraft_config['host']

        if self.__minecraft_config['username'] is not None:
            container_envs["MINECRAFT_USERNAME"] = self.__minecraft_config[
                'username']

        if self.__minecraft_config['password'] is not None:
            container_envs["MINECRAFT_PASSWORD"] = self.__minecraft_config[
                'password']

        if self.__minecraft_config['port'] is not None:
            container_envs["MINECRAFT_PORT"] = self.__minecraft_config['port']

        if self.__minecraft_config['version'] is not None:
            container_envs["MINECRAFT_VERSION"] = self.__minecraft_config[
                'version']

        if self.__minecraft_config['auth'] is not None:
            container_envs["MINECRAFT_AUTH"] = self.__minecraft_config['auth']

        container_envs["AGENT_NAME"] = name

        for blueprint_env in blueprint.environment_variables:
            if blueprint_env not in container_envs:
                container_envs[
                    blueprint_env] = blueprint.environment_variables[
                        blueprint_env]

        agent_container = self.__get_docker_client().containers.create(
            blueprint.image,
            name=name,
            detach=True,
            environment=container_envs,
            network="bridge")

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
            print(f"Agent with name '{name}' not found!")
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
            print(f"Agent with name '{name}' not found!")
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
            print(f"Agent with name '{name}' not found!")
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
            print(f"Agent with name '{name}' not found!")
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
            print(f"Agent with name '{name}' not found!")
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
            print(f"Agent with name '{name}' not found!")
            return None

        agent = Agent(container, self)

        # UPDATE CACHE
        #   when container exists but cache has no entry for it,
        #   add it to cache
        if not self.__cache.has(name):
            self.__cache.add(agent)

        return agent

    def generate_blueprint(self, agent_source_path: str) -> AgentBlueprint:
        """
        Create a new blueprint for agents based on agent_source_path
        """
        image = self.__get_docker_client().images.build(path=agent_source_path,
                                                        rm=True)
        blueprint = AgentBlueprint(image[0])

        return blueprint
