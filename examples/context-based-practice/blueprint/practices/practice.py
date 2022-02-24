from abc import abstractmethod
from datetime import datetime
from typing import Dict, List
from vector3 import Vector3
import math
from perceptions import Perception, Block


class Perceptron:
    def __init__(self, label: str, weight: float, bias: float = 0) -> None:
        self.__label = label
        self.__weigth = weight
        self.__bias = bias

    @property
    def label(self) -> str:
        return self.__label

    @property
    def weight(self) -> float:
        return self.__weigth

    @property
    def bias(self) -> float:
        return self.__bias

    def __str__(self) -> str:
        return f"{self.label}, x{self.weight}, +{self.bias}"


class Context:
    __indexed_by_label: Dict[str, List[Perception]]
    __indexed_by_blocks: Dict[str, List[Block]]

    def __init__(self) -> None:
        self.__indexed_by_label = {}
        self.__indexed_by_blocks = {}

    def add_perception(self, perception: Perception) -> None:
        if perception.salience <= 0:
            return

        if perception.label not in self.__indexed_by_label:
            self.__indexed_by_label[perception.label] = []
        self.__indexed_by_label[perception.label].append(perception)

    def add_block_perception(self, block_perception: Perception) -> None:
        if block_perception.salience <= 0:
            return

        if block_perception.label != "BLOCK" or not isinstance(block_perception.target, Block):
            raise Exception()

        self.add_perception(block_perception)

        if block_perception.target.type not in self.__indexed_by_blocks:
            self.__indexed_by_blocks[block_perception.target.type] = []

        self.__indexed_by_blocks[block_perception.target.type].append(block_perception.target)

    def get_perceptions_by_label(self, label: str) -> List[Perception]:
        if label in self.__indexed_by_label:
            return self.__indexed_by_label[label]
        return []

    def get_block_positions_by_type(self, block_type: str) -> List[Block]:
        if block_type in self.__indexed_by_blocks:
            return self.__indexed_by_blocks[block_type]
        return []

    def get_perceptions(self) -> List[Perception]:
        all_perceptions = []
        for _, perceptions in self.__indexed_by_label.items():
            all_perceptions.extend(perceptions)
        return all_perceptions


class Practice:

    __perceptrons: List[Perceptron]

    def __init__(self, bot, perceptrons: List[Perceptron], name: str, timeout: float = 20) -> None:
        self.__perceptrons = perceptrons
        self.__salience = 0
        self.__name = name
        self._bot = bot
        self.__start_time = None
        self.__timeout = timeout

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def update_salience(self, context: Context) -> float:
        new_salience = 0

        for perceptron in self.__perceptrons:
            perceptions = context.get_perceptions_by_label(perceptron.label)
            for perception in perceptions:

                new_salience += perceptron.weight * perception.salience + perceptron.bias

        new_salience = Practice.sigmoid(new_salience)
        delta = new_salience - self.__salience
        self.__salience = new_salience
        return delta

    @property
    def salience(self) -> float:
        return self.__salience

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def is_possible(self) -> bool:
        pass

    @abstractmethod
    def has_ended(self) -> bool:
        return (datetime.now() - self.__start_time).total_seconds() > self.__timeout

    @abstractmethod
    def setup(self, context: Context) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        self.__start_time = datetime.now()
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.__name} [{self.__salience}]"
