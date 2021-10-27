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
        pass

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
            agents.append(Agent(agent_container))

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
            self.__cache.erase(container.id)
            container.remove(force=True)

        except docker.errors.NotFound:
            print("Agent not found")

    def deploy_agent(self, name: str) -> None:
        '''
        Deploys a previously created agent to the Minecraft Server
        '''
        try:
            self.__get_docker_container(name).start()

        except docker.errors.NotFound:
            print("Agent not found")

    def withdraw_agent(self, name: str) -> None:
        '''
        Withdraws a previously deployed agent from the Minecraft Server
        '''
        try:
            self.__get_docker_container(name).stop()

        except docker.errors.NotFound:
            print("Agent not found")

    def pause_agent(self, name: str) -> None:
        '''
        Pauses a previously deployed agent execution
        '''
        try:
            self.__get_docker_container(name).pause()

        except docker.errors.NotFound:
            print("Agent not found")

    def resume_agent(self, name: str) -> None:
        '''
        Resumes a previously paused agent
        '''
        try:
            self.__get_docker_container(name).unpause()

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

            return Agent(container)

        except docker.errors.NotFound:
            print("Agent not found")


class AgentCache:
    def __init__(self):
        self.__cache = {}

    def add(self, agent: Agent) -> str:
        '''
        Add agent to the cache.

        returns the cache ID Entry
        '''
        if self.has(agent.id):
            return
        self.__cache[agent.id] = agent

        return agent.id

    def get(self, id: str) -> Optional[Agent]:
        '''
        Retrieves the agent by id
        '''
        if not self.has(id):
            return None
        return self.__cache[id]

    def has(self, id: str) -> bool:
        '''
        Tests if the cache has agent with 'id'
        '''
        return id in self.__cache

    def erase(self, id: str) -> None:
        '''
        Remove entry with id
        '''
        if not self.has(id):
            return

        self.__cache.pop(id)