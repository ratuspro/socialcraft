'''
This module defines the AgentManager class
'''
import pathlib
from typing import Optional
import docker
from docker.models.containers import Container
from docker.client import DockerClient
from core.agent import Agent


class AgentManager:
    '''
    The AgentManager class supervises the deployment of agents
    
    '''
    def __init__(self, docker_url=None):
        self.__cache = AgentCache()
        if docker_url is not None:
            self.__docker_client = docker.DockerClient(base_url=docker_url)
        else:
            self.__docker_client = docker.from_env()

    def __get_docker_client(self) -> Optional[DockerClient]:
        return self.__docker_client

    def __get_docker_container(self, name: str) -> Optional[Container]:
        try:
            return self.__get_docker_client().containers.get(name)
        except docker.errors.NotFound:
            return None

    def get_all_agents(self) -> list[Agent]:
        '''
        List all the agents available
        '''
        agent_containers = self.__get_docker_client().containers.list(
            all=True, filters={'label': ["socialcraft_agent"]})

        agents = []

        for agent_container in agent_containers:
            if self.__cache.has(agent_container.name):
                agents.append(self.__cache.get(agent_container.name))
            else:
                agent = Agent(agent_container)
                self.__cache.add(agent)
                agents.append(agent)

        return agents

    def create_agent(self, name: str) -> Optional[Agent]:
        '''
        Creates a new agent based on a previously created prototype
        '''
        container = self.__get_docker_container(name)

        if container is not None:
            print(f"Agent with name '{name}' already exists.")
            return None

        # when agent does not exist and cache has an entry for it, clean cache
        if self.__cache.has(name):
            self.__cache.erase(name)

        path = pathlib.Path(pathlib.Path().resolve(),
                            "example/images/simple_bot/")
        image = self.__get_docker_client().images.build(path=str(path))
        agent_container = self.__get_docker_client().containers.create(
            image[0],
            'sleep 300',
            name=name,
            labels=["socialcraft_agent"],
            detach=True)

        agent = Agent(agent_container)
        self.__cache.add(agent)
        return agent

    def kill_agent(self, name: str) -> None:
        '''
        Permanentely kills an agent and destroys all associated data
        '''
        # UPDATE CACHE
        #   when agent should be killed and cache has an entry for it, clean cache
        if self.__cache.has(name):
            self.__cache.erase(name)

        container = self.__get_docker_container(name)

        if container is None:
            print(f"Agent with name '{name}' not found!")
            return

        container.remove(force=True)

    def deploy_agent(self, name: str) -> None:
        '''
        Deploys a previously created agent to the Minecraft Server
        '''

        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it, clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            print(f"Agent with name '{name}' not found!")
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it, add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container))

        container.start()

    def withdraw_agent(self, name: str) -> None:
        '''
        Withdraws a previously deployed agent from the Minecraft Server
        '''
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it, clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            print(f"Agent with name '{name}' not found!")
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it, add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container))

        container.stop()

    def pause_agent(self, name: str) -> None:
        '''
        Pauses a previously deployed agent execution
        '''
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it, clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            print(f"Agent with name '{name}' not found!")
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it, add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container))

        container.pause()

    def resume_agent(self, name: str) -> None:
        '''
        Resumes a previously paused agent
        '''
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it, clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            print(f"Agent with name '{name}' not found!")
            return

        # UPDATE CACHE
        #   when container exists but cache has no entry for it, add it to cache
        if not self.__cache.has(name):
            self.__cache.add(Agent(container))

        container.unpause()

    def get_agent(self, name: str) -> Optional[Agent]:
        '''
        Retrieves the agent with 'name'
        '''
        container = self.__get_docker_container(name)

        if container is None:
            # UPDATE CACHE
            #   when container does not exist but cache has an entry for it, clean cache
            if self.__cache.has(name):
                self.__cache.erase(name)
            print(f"Agent with name '{name}' not found!")
            return None

        agent = Agent(Container)

        # UPDATE CACHE
        #   when container exists but cache has no entry for it, add it to cache
        if not self.__cache.has(name):
            self.__cache.add(agent)

        return agent


class AgentCache:
    def __init__(self):
        self.__cache = {}

    def add(self, agent: Agent) -> str:
        '''
        Add agent to the cache.

        returns the cache name Entry
        '''
        if self.has(agent.name):
            return
        self.__cache[agent.name] = agent

        return agent.name

    def get(self, name: str) -> Optional[Agent]:
        '''
        Retrieves the agent by name
        '''
        if not self.has(name):
            return None
        return self.__cache[name]

    def has(self, name: str) -> bool:
        '''
        Tests if the cache has agent with 'name'
        '''
        return name in self.__cache

    def erase(self, name: str) -> None:
        '''
        Remove entry with name
        '''
        if not self.has(name):
            return

        self.__cache.pop(name)