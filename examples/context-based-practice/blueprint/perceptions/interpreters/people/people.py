from abc import ABC, abstractclassmethod
from typing import List
from ...models import Player, Perception
from vector3 import Vector3


class PeopleInterpreter(ABC):
    @abstractclassmethod
    def interpret(self, bot, players) -> List[Perception]:
        return []


class PeopleCloseBy(PeopleInterpreter):
    __distance_squared: float
    perception_label: str

    def __init__(self, distance: float, perception_label: str) -> None:
        super().__init__()
        self.__distance_squared = distance * distance
        self.__perception_label = perception_label

    def interpret(self, bot, players: List[Player]) -> List[Perception]:
        position = Vector3(bot.entity.position)
        for player in players:
            if player.position.distanceSquaredTo(position) < self.__distance_squared:
                return [Perception(self.__perception_label, 1, None)]
        return []


class PeopleInterpreterManager:

    __interpreters: List[PeopleInterpreter]

    def __init__(self, bot) -> None:
        self.__interpreters = []
        self.__bot = bot

    def add_interpreter(self, interpreter: PeopleInterpreter):
        self.__interpreters.append(interpreter)

    def process(self, players) -> List[Perception]:
        perceptions = []
        for interpreter in self.__interpreters:
            perceptions.extend(interpreter.interpret(self.__bot, players))
        return perceptions
