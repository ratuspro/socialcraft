from abc import ABC, abstractmethod

import csf.core


class Interpreter(ABC):
    @abstractmethod
    def process_perceptions(self, perceptions: csf.core.Context) -> list[csf.core.Perception]:
        pass
