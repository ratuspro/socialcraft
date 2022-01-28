from abc import ABC, abstractmethod
from pyclbr import Function
import string
from typing import Any, Callable, Literal
from unicodedata import name
from .frames import CognitiveSocialFrame


class Perception:
    def __init__(self, name: str, value: Any) -> None:
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> Any:
        return self.__value

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.value)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Perception):
            return False
        return self.__name == o.name and self.__value == o.value

    def __str__(self) -> str:
        return f"<name: {self.name}, value: {str(self.value)}>"


class Affordance:
    def __init__(self, name: str, value: Any, salience: float) -> None:
        self.__name = name
        self.__value = value
        self.__salience = salience

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> Any:
        return self.__value

    @property
    def value(self) -> Any:
        return self.__salience

    def __repr__(self) -> str:
        return f"{self.__name}[{self.__salience}]({str(self.__value)})"


class Context:
    def __init__(self) -> None:
        self.__perceptions = {}

    def get_perception(self, name: string) -> Perception | None:
        if name in self.__perceptions:
            return self.__perceptions[name]
        return None

    def get_perceptions(self) -> set[Perception]:
        return list(self.__perceptions.values())

    def add_perception(self, perception: Perception) -> None:
        self.__perceptions[perception.name] = perception

    def add_perceptions(self, perceptions: set[Perception]) -> None:
        for perception in perceptions:
            self.__perceptions[perception.name] = perception


class Interpreter(ABC):
    @abstractmethod
    def process_perceptions(self, perceptions: list[Perception]) -> list[Perception]:
        pass


class Brain:
    __frames: set[CognitiveSocialFrame]
    __perception_buffer: set[Perception]
    __salient_frames: set[CognitiveSocialFrame]
    __interpreters: set[Interpreter]

    def __init__(self) -> None:
        self.__frames = set()
        self.__perception_buffer = set()
        self.__salient_frames = set()
        self.__interpreters = set()

    def add_frame(self, frame: CognitiveSocialFrame) -> None:
        self.__frames.add(frame)

    def add_perception_to_buffer(self, perception: Perception) -> None:
        self.__perception_buffer.add(perception)

    def add_interpreter(self, interpreter: Interpreter) -> None:
        self.__interpreters.add(interpreter)

    def update_saliences(self) -> None:
        self.__salient_frames.clear()

        context = Context()
        for perception in self.__perception_buffer:
            context.add_perception(perception)

        perceptions = context.get_perceptions()
        for interpreter in self.__interpreters:
            context.add_perceptions(interpreter.process_perceptions(perceptions))

        print("dasasda")

        for perception in context.get_perceptions():
            print(perception)

        for frame in self.__frames:
            if frame.is_salient(context):
                self.__salient_frames.add(frame)

        self.__perception_buffer.clear()

    def get_affordances(self) -> list[Affordance]:
        affordances = set()
        for sal_frame in self.__salient_frames:
            affordances = affordances.union(sal_frame.get_affordances())

        return affordances
