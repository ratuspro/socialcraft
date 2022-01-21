from pyclbr import Function
import string
from typing import Any, Callable, Literal
from unicodedata import name
from frames.cogntive_social_frame import CognitiveSocialFrame


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

    def get_perception(self, name: string) -> Any | None:
        if name in self.__perceptions:
            return self.__perceptions[name]
        return None

    def add_perception(self, perception: Perception) -> None:
        self.__perceptions[perception.name] = perception.value


class Brain:
    def __init__(self) -> None:
        self.__frames = set()
        self.__perception_buffer = set()
        self.__salient_frames = set()

    def add_frame(self, frame: CognitiveSocialFrame) -> None:
        self.__frames.add(frame)

    def add_perception_to_buffer(self, perception: Perception) -> None:
        self.__perception_buffer.add(perception)

    def update_saliences(self) -> None:
        self.__salient_frames.clear()

        context = Context()
        for perception in self.__perception_buffer:
            context.add_perception(perception)

        for frame in self.__frames:
            if frame.is_salient(context):
                self.__salient_frames.add(frame)

        self.__perception_buffer.clear()

    def get_affordances(self) -> list[Affordance]:
        affordances = set()
        for sal_frame in self.__salient_frames:
            affordances = affordances.union(sal_frame.get_affordances())

        return affordances
