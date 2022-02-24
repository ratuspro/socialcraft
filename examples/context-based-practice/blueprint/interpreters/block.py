from abc import ABC, abstractclassmethod
from typing import List
from practices import Perception, Block


class BlockInterpreter(ABC):
    @abstractclassmethod
    def interpret(self, bot, blocks: List[Block]) -> List[Perception]:
        return []


class BlockInterpreterManager:

    __interpreters: List[BlockInterpreter]

    def __init__(self, bot) -> None:
        self.__interpreters = []
        self.__bot = bot

    def add_interpreter(self, interpreter: BlockInterpreter):
        self.__interpreters.append(interpreter)

    def process(self, blocks: List[Block]) -> List[Perception]:
        perceptions = []
        for interpreter in self.__interpreters:
            perceptions.extend(interpreter.interpret(self.__bot, blocks))
        return perceptions


class WoodCloseBy(BlockInterpreter):
    def interpret(self, bot, blocks: List[Block]) -> List[Perception]:
        wood_types = ["Oak Log"]
        for block in blocks:
            if block.type in wood_types:
                return [Perception("WOOD_IN_SIGHT", 1)]
        return []
