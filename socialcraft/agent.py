"""
This module defines an Agent and the respective types (AgentStatus)
"""
from enum import Enum
from docker.models.containers import Container


class AgentStatus(Enum):
    """
    The status of an agent
    """

    OFFLINE = 1
    ONLINE = 2
    PAUSED = 3


class Agent:
    """
    The Agent class is a proxy to control the agent
    """

    def __init__(self, container: Container, manager):
        self.__container = container
        self.__manager = manager

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Container):
            return False

        return self.identifier == other.id

    @property
    def status(self):
        """
        The status of the agent
        """
        if self.__container.status in (
            "created",
            "restarting",
            "removing",
            "exited",
        ):
            return AgentStatus.OFFLINE

        if self.__container.status == "running":
            return AgentStatus.ONLINE

        if self.__container.status == "paused":
            return AgentStatus.PAUSED

    @property
    def name(self):
        """
        The name of the agent
        """
        return self.__container.name

    @property
    def identifier(self):
        """
        The agent's identifier
        """
        return self.__container.id

    def pause(self):
        """
        Pauses this agent execution
        """
        self.__manager.pause_agent(self.name)

    def resume(self):
        """
        Resumes this agent execution
        """
        self.__manager.resume_agent(self.name)

    def deploy(self):
        """
        Deploys this agent to server
        """
        self.__manager.deploy_agent(self.name)

    def withdraw(self):
        """
        Withdraws this agent from server
        """
        self.__manager.withdraw_agent(self.name)

    def kill(self):
        """
        Kills this agent
        """
        self.__manager.kill_agent(self.name)
