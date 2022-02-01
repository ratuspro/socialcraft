from typing import Any
from . import core

from . import practices
from . import interpreters
from . import frames


class Brain:
    __frames: set[frames.CognitiveSocialFrame]
    __perception_buffer: set[core.Perception]
    __salient_frames: set[frames.CognitiveSocialFrame]
    __interpreters: set[interpreters.Interpreter]

    def __init__(self) -> None:
        self.__frames = set()
        self.__perception_buffer = set()
        self.__salient_frames = set()
        self.__interpreters = set()
        self.__lastContext = None

    def add_frame(self, frame: frames.CognitiveSocialFrame) -> None:
        self.__frames.add(frame)

    def add_perception_to_buffer(self, perception: core.Perception) -> None:
        self.__perception_buffer.add(perception)

    def add_interpreter(self, interpreter: interpreters.Interpreter) -> None:
        self.__interpreters.add(interpreter)

    def get_last_context(self) -> core.Context:
        return self.__lastContext

    def update_saliences(self) -> None:
        self.__salient_frames.clear()

        context = core.Context()
        context.add_perceptions(self.__perception_buffer)

        for interpreter in self.__interpreters:
            context.add_perceptions(interpreter.process_perceptions(context))

        self.__lastContext = context

        for frame in self.__frames:
            if frame.is_salient(context):
                self.__salient_frames.add(frame)

        self.__perception_buffer.clear()

    def get_affordances(self) -> list[practices.Practice]:
        affordances = set()
        for sal_frame in self.__salient_frames:
            affordances = affordances.union(sal_frame.get_affordances())

        return list(affordances)
