from abc import abstractmethod
from datetime import datetime
from typing import Dict, List
from vector3 import Vector3
import math


class Player:

    __name: str
    __position: Vector3

    def __init__(self, name: str, position: Vector3) -> None:
        self.__name = name
        self.__position = position

    @property
    def name(self) -> str:
        return self.__name

    @property
    def position(self) -> Vector3:
        return self.__position

    def __str__(self) -> str:
        return f"Player {self.__name} at {self.__position}"


class Block:
    __type: str
    __position: Vector3

    def __init__(self, type: str, position: Vector3) -> None:
        self.__type = type
        self.__position = position

    @property
    def type(self) -> str:
        return self.__type

    @property
    def position(self) -> Vector3:
        return self.__position

    def __str__(self) -> str:
        return f"Player {self.__type} at {self.__position}"


class Perception:
    def __init__(self, label: str, value: float) -> None:
        self.__label = label
        self.__value = value

    @property
    def label(self) -> str:
        return self.__label

    @property
    def value(self) -> float:
        return self.__value

    def __str__(self) -> str:
        return f"{self.label} => {self.value}"


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
        if perception.label not in self.__indexed_by_label:
            self.__indexed_by_label[perception.label] = []
        self.__indexed_by_label[perception.label].append(perception)

    def add_block_perception(self, block_perception: Perception) -> None:
        if block_perception.label != "BLOCK" or not isinstance(block_perception.value, Block):
            raise Exception()

        self.add_perception(block_perception)

        if block_perception.value.type not in self.__indexed_by_blocks:
            self.__indexed_by_blocks[block_perception.value.type] = []

        self.__indexed_by_blocks[block_perception.value.type].append(block_perception.value)

    def get_perceptions_by_label(self, label: str) -> List[Perception]:
        if label in self.__indexed_by_label:
            return self.__indexed_by_label[label]
        return []

    def get_block_positions_by_type(self, block_type: str) -> List[Vector3]:
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

                new_salience += perceptron.weight * perception.value + perceptron.bias

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
