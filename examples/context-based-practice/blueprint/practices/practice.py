from abc import abstractmethod
from datetime import datetime


class PerceptionLabel:
    TIME = 0
    WEEKDAY = 1
    RAIN = 2
    THUNDER = 3
    ISDAY = 4
    ISNIGHT = 5
    OWNBEDVISIBLE = 6

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


class Practice:
    def __init__(self, bot, percepton: list[Perceptron], name: str, timeout: float = 20) -> None:
        self.__percepton = percepton
        self.__salience = 0
        self.__name = name
        self._bot = bot
        self.__start_time = None
        self.__timeout = timeout

    def update_salience(self, perceptions: dict[PerceptionLabel, float]) -> float:
        new_salience = 0
        for percepton in self.__percepton:
            if percepton.label in perceptions.keys():
                new_salience += percepton.weight * perceptions[percepton.label] + percepton.bias

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
    def setup(self) -> None:
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
