'''
This module defines an Agent and the respective types (AgentStatus)
'''
from enum import Enum
from docker.models.containers import Container


class AgentStatus(Enum):
    '''
    The status of an agent
    '''
    OFFLINE = 1
    ONLINE = 2
    PAUSED = 3


class Agent:
    '''
    The Agent class is a proxy to control the agent
    '''
    def __init__(self, container: Container):
        self.__container = container

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Container):
            return False

        return self.id == other.id

    @property
    def status(self):
        '''
        The status of the agent
        '''
        if self.__container.status in ('created', 'restarting', 'removing',
                                       'exited'):
            return AgentStatus.OFFLINE

        if self.__container.status == 'running':
            return AgentStatus.ONLINE

        if self.__container.status == 'paused':
            return AgentStatus.PAUSED

    @property
    def name(self):
        '''
        The name of the agent
        '''
        return self.__container.name

    @property
    def id(self):
        '''
        The agent's identifier
        '''
        return self.__container.id
