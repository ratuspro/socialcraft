from abc import ABC, abstractclassmethod
from typing import List
from ...models import Block, Perception


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


class IsBlockCloseBy(BlockInterpreter):
    __label: str
    __block_types: List[str]

    def __init__(self, label: str, block_types: List[str]) -> None:
        super().__init__()
        self.__label = label
        self.__block_types = block_types

    def interpret(self, bot, blocks: List[Block]) -> List[Perception]:
        for block in blocks:
            if block.type in self.__block_types:
                return [Perception(self.__label, 1, None)]
        return []
