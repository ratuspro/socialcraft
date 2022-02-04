from abc import abstractmethod, ABC
import logging
import sys


class Practice(ABC):
    def __init__(self, creator) -> None:
        self._creator = creator

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    def is_valid(self, context) -> bool:
        return self._creator.is_salient(context)
