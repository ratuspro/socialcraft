from abc import abstractmethod
from datetime import datetime
from typing import Dict, List


class PerceptionLabel:
    TIME = 0
    WEEKDAY = 1
    RAIN = 2
    THUNDER = 3
    ISDAY = 4
    ISNIGHT = 5
    OWNBEDVISIBLE = 6
    WOODINSIGHT = 7
    BLOCK = 8
    PLAYER = 9


class Perception:
    def __init__(self, label: PerceptionLabel, value: float) -> None:
        self.__label = label
        self.__value = value

    @property
    def label(self) -> PerceptionLabel:
        return self.__label

    @property
    def value(self) -> float:
        return self.__value

    def __str__(self) -> str:
        return f"{self.label} => {self.value}"


class Perceptron:
    def __init__(self, label: PerceptionLabel, weight: float, bias: float = 0) -> None:
        self.__label = label
        self.__weigth = weight
        self.__bias = bias

    @property
    def label(self) -> PerceptionLabel:
        return self.__label

    @property
    def weight(self) -> float:
        return self.__weigth

    @property
    def bias(self) -> float:
        return self.__bias


class Context:
    __indexed_by_label: Dict[str, List[Perception]]

    def __init__(self) -> None:
        self.__indexed_by_label = {}

    def add_perception(self, perception: Perception) -> None:
        if perception.label not in self.__indexed_by_label:
            self.__indexed_by_label[perception.label] = []
        self.__indexed_by_label[perception.label].append(perception)

    def get_perceptions_by_label(self, label: str) -> List[Perception]:
        if label in self.__indexed_by_label:
            return self.__indexed_by_label[label]
        return []

    def get_perceptions(self) -> List[str]:
        all_perceptions = []
        for _, perceptions in self.__indexed_by_label.items():
            all_perceptions.extend(perceptions)

        for p in all_perceptions:
            print(p)
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

    def update_salience(self, context: Context) -> float:
        new_salience = 0

        for perceptron in self.__perceptrons:
            perceptions = context.get_perceptions_by_label(perceptron.label)
            for perception in perceptions:
                new_salience += perceptron.weight * perception.value + perceptron.bias

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
