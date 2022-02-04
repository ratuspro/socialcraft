import logging
import sys

from . import core
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

        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

    def add_frame(self, frame: frames.CognitiveSocialFrame) -> None:
        self.__logger.debug(f"Add new frame: {frame}")
        self.__frames.add(frame)

    def add_perception_to_buffer(self, perception: core.Perception) -> None:
        self.__logger.debug(f"Add perception to buffer: {perception}")
        self.__perception_buffer.add(perception)

    def add_interpreter(self, interpreter: interpreters.Interpreter) -> None:
        self.__logger.debug(f"Add interpreter to buffer: {interpreter}")
        self.__interpreters.add(interpreter)

    def get_last_context(self) -> core.Context:
        return self.__lastContext

    def update_saliences(self) -> None:
        self.__logger.debug(f"Updating saliences...")
        self.__salient_frames.clear()

        self.__logger.debug(f"Creating new context...")
        context = core.Context()
        if len(self.__perception_buffer) == 0:
            self.__logger.debug(f"No perceptions on buffer.")
        else:
            for perception in self.__perception_buffer:
                self.__logger.debug(f"Added perception {perception} to context")
            context.add_perceptions(self.__perception_buffer)

        self.__logger.debug(f"Apply interpreters to context...")
        for interpreter in self.__interpreters:
            self.__logger.debug(f"Apply interpreter {interpreter}")
            new_perceptions = interpreter.process_perceptions(context)

            if len(new_perceptions) == 0:
                self.__logger.debug(f"No interpreted perceptions added!")
            else:
                for new_perception in new_perceptions:
                    self.__logger.debug(f"Added interpreted perception {new_perception}")

            context.add_perceptions(new_perceptions)

        self.__lastContext = context

        self.__logger.debug(f"Update frames' saliences...")
        for frame in self.__frames:
            if frame.is_salient(context):
                self.__logger.debug(f"Frame {frame} is salient.")
                self.__salient_frames.add(frame)
            else:
                self.__logger.debug(f"Frame {frame} is not salient.")

        self.__perception_buffer.clear()
        self.__logger.debug(f"Cleared perception's buffer.")

    def get_affordances(self) -> list[core.Affordance]:
        affordances = set()
        for sal_frame in self.__salient_frames:
            affordances = affordances.union(sal_frame.get_affordances())

        return list(affordances)
