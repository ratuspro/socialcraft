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
    def __init__(self):
        self.__cache = AgentCache()

    def __get_docker_client(self) -> Optional[DockerClient]:
        return docker.from_env()

    def __get_docker_container(self, name: str) -> Container:
        return self.__get_docker_client().containers.get(name)

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
        try:
            container = self.__get_docker_container(name)
            self.__cache.erase(container.name)
            container.remove(force=True)

        except docker.errors.NotFound:
            print("Agent not found")

    def deploy_agent(self, name: str) -> None:
        '''
        Deploys a previously created agent to the Minecraft Server
        '''
        try:
            container = self.__get_docker_container(name)
            container.start()

            if not self.__cache.has(name):
                self.__cache.add(Agent(container))

        except docker.errors.NotFound:
            print("Agent not found")

    def withdraw_agent(self, name: str) -> None:
        '''
        Withdraws a previously deployed agent from the Minecraft Server
        '''
        try:
            container = self.__get_docker_container(name)
            container.stop()

            if not self.__cache.has(name):
                self.__cache.add(Agent(container))

        except docker.errors.NotFound:
            print("Agent not found")

    def pause_agent(self, name: str) -> None:
        '''
        Pauses a previously deployed agent execution
        '''
        try:
            container = self.__get_docker_container(name)
            container.pause()

            if not self.__cache.has(name):
                self.__cache.add(Agent(container))

        except docker.errors.NotFound:
            print("Agent not found")

    def resume_agent(self, name: str) -> None:
        '''
        Resumes a previously paused agent
        '''
        try:
            container = self.__get_docker_container(name)
            container.unpause()

            if not self.__cache.has(name):
                self.__cache.add(Agent(container))

        except docker.errors.NotFound:
            print("Agent not found")

    def get_agent(self, name: str) -> Optional[Agent]:
        '''
        Retrieves the agent with 'name'
        '''
        try:
            container = self.__get_docker_container(name)

            if self.__cache.has(container.id):
                return self.__cache.get(container.id)
            else:
                agent = Agent(container)
                self.__cache.add(agent)

            return agent

        except docker.errors.NotFound:
            print("Agent not found")


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