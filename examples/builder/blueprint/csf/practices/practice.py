from abc import abstractmethod, ABC
import logging
from sre_parse import State
import sys
import enum


class Practice(ABC):
    class State(enum.Enum):
        CREATED = 1
        RUNNING = 2
        STOPPED = 3
        FINISHED = 4

    def __init__(self, creator) -> None:
        self._creator = creator
        self._state = Practice.State.CREATED

    @property
    def state(self):
        return self._state

    @abstractmethod
    def start(self) -> None:
        pass

    def update(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    def is_valid(self, context) -> bool:
        return self._creator.is_salient(context)

    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass
