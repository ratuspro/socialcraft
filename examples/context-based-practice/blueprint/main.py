from abc import abstractclassmethod, abstractmethod
import math
import logging
import sys
from datetime import datetime
from javascript import On, require, start, AsyncTask, stop, eval_js
from socialcraft_handler import Socialcraft_Handler
from vector3 import Vector3

pathfinder = require("mineflayer-pathfinder")

# Init Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

bot = handler.bot


class PerceptionLabel:
    TIME = 0
    WEEKDAY = 1
    RAIN = 2
    THUNDER = 3
    C0_NUMBER_PEOPLE = 4


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


class Percepton:
    def __init__(self, label: PerceptionLabel, weight: float) -> None:
        self.__label = label
        self.__weigth = weight

    @property
    def label(self) -> PerceptionLabel:
        return self.__label

    @property
    def weight(self) -> float:
        return self.__weigth


class Practice:
    def __init__(self, bot, percepton: list[Percepton], name: str) -> None:
        self.__percepton = percepton
        self.__salience = 0
        self.__name = name
        self._bot = bot
        self.__start_time = None

    def update_salience(self, perceptions: dict[PerceptionLabel, float]) -> float:
        new_salience = 0
        for percepton in self.__percepton:
            if percepton.label in perceptions.keys():
                new_salience += percepton.weight * perceptions[percepton.label]

        delta = new_salience - self.__salience
        self.__salience = new_salience
        return delta

    @property
    def salience(self):
        return self.__salience

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def has_ended(self) -> bool:
        return (datetime.now() - self.__start_time).total_seconds() > 20

    @abstractmethod
    def start(self):
        self.__start_time = datetime.now()
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    def __str__(self) -> str:
        return f"{self.__name} [{self.__salience}]"


class AvoidPeoplePractice(Practice):
    def __init__(self, bot, percepton: list[Percepton]) -> None:
        super().__init__(bot, percepton, "AvoidPeoplePractice")
        self.__target_position = None

    def start(self):
        super().start()
        bot_position = Vector3(self._bot.entity.position)
        nearest_target_position = Vector3(self._bot.nearestEntity(lambda entity: entity.type == "player").position)
        self.__target_position = (
            nearest_target_position.subtract(bot_position).normalize().multiply(Vector3(5, 0, 5)).add(bot_position)
        )
        goal = pathfinder.goals.GoalNearXZ(self.__target_position.x, self.__target_position.z, 0.5)
        self._bot.pathfinder.setGoal(goal)

    def update(self):
        super().update()

    def has_ended(self) -> bool:
        return super().has_ended() or self.__target_position.xzDistanceTo(Vector3(self._bot.entity.position)) < 1

    def exit(self):
        super().exit()
        self._bot.pathfinder.setGoal(None)


practices = [
    AvoidPeoplePractice(
        bot,
        [
            Percepton(label=PerceptionLabel.C0_NUMBER_PEOPLE, weight=1),
        ],
    )
]


@AsyncTask(start=True)
def async_basic_agent_loop(task):

    best_practice = None

    while not task.stopping:

        logger.info(f"Start Agent Loop at {bot.time.time}")
        start_time = datetime.now()

        # Perceive
        perceptions = {}
        perceptions[PerceptionLabel.TIME] = bot.time.time / 24000
        perceptions[PerceptionLabel.WEEKDAY] = bot.time.day % 7
        perceptions[PerceptionLabel.RAIN] = bot.rainState
        perceptions[PerceptionLabel.THUNDER] = bot.thunderState
        nearest_player_position = bot.nearestEntity().position
        perceptions[PerceptionLabel.C0_NUMBER_PEOPLE] = (
            1 if nearest_player_position.xzDistanceTo(bot.entity.position) < 5 else 0
        )

        print(perceptions)
        # Update Practice
        for practice in practices:
            practice.update_salience(perceptions)
        practices.sort(reverse=True, key=lambda practice: practice.salience)

        if best_practice is not None:
            if best_practice.has_ended():
                print(f"Exit Practice")
                best_practice.exit()
                best_practice = None
            else:
                print("Update Practice")
                best_practice.update()
        else:
            if practices[0].salience > 0:
                print("Start Practice")
                best_practice = practices[0]
                best_practice.start()
            else:
                print("Do nothing")

        time_spent = datetime.now() - start_time
        milliseconds = (time_spent.days * 24 * 60 * 60 + time_spent.seconds) * 1000 + time_spent.microseconds / 1000.0
        logger.info(f"Last update took {milliseconds} miliseconds")

        if milliseconds < 1000:
            time_to_wait = 1000 - int(milliseconds)
            logger.info(f"Waiting {time_to_wait} miliseconds")

            task.wait(time_to_wait / 1000)


@On(bot, "time")
def handleTick(_):
    pass
