import random
from tracemalloc import start

from setuptools import setup
from vector3 import Vector3
from .practice import Practice, Perceptron

from javascript import require, eval_js

pathfinder = require("mineflayer-pathfinder")

Vec3 = require("vec3")


class AvoidPeoplePractice(Practice):
    def __init__(self, bot, percepton: list[Perceptron]) -> None:
        super().__init__(bot, percepton, "AvoidPeoplePractice")
        self.__target_position = None

    def setup(self) -> None:
        super().setup()
        bot_position = Vector3(self._bot.entity.position)
        nearest_target_position = Vector3(self._bot.nearestEntity(lambda entity: entity.type == "player").position)
        self.__target_position = (
            nearest_target_position.subtract(bot_position).normalize().multiply(Vector3(5, 0, 5)).add(bot_position)
        )

    def start(self):
        super().start()
        goal = pathfinder.goals.GoalNearXZ(self.__target_position.x, self.__target_position.z, 0.5)
        self._bot.pathfinder.setGoal(goal)

    def update(self):
        super().update()

    def is_possible(self) -> bool:
        return True

    def has_ended(self) -> bool:
        return super().has_ended() or self.__target_position.xzDistanceTo(Vector3(self._bot.entity.position)) < 1

    def exit(self):
        super().exit()
        self._bot.pathfinder.setGoal(None)


class GoToHousePractice(Practice):

    __target_bed: Vector3

    def __init__(self, bot, percepton: list[Perceptron]) -> None:
        super().__init__(bot, percepton, "GoToHousePractice")
        self.__target_bed = None

    def setup(self) -> None:
        super().setup()
        self.__target_bed = self._bot.kb["bed_position"]

    def start(self):
        super().start()
        goal = pathfinder.goals.GoalNear(self.__target_bed.x, self.__target_bed.y, self.__target_bed.z, 0.5)
        self._bot.pathfinder.setGoal(goal)

    def update(self):
        super().update()

    def is_possible(self) -> bool:
        return True

    def has_ended(self) -> bool:
        return super().has_ended() or self.__target_bed.distanceTo(Vector3(self._bot.entity.position)) < 1

    def exit(self):
        super().exit()
        self._bot.pathfinder.setGoal(None)


class SleepPractice(Practice):

    __target_bed: Vector3

    def __init__(self, bot, percepton: list[Perceptron]) -> None:
        super().__init__(bot, percepton, "SleepPractice")
        self.__target_bed = None

    def setup(self):
        super().setup()
        self.__target_bed = self._bot.kb["bed_position"]

    def start(self):
        super().start()
        self.__target_bed = self._bot.kb["bed_position"]
        goal = pathfinder.goals.GoalNear(self.__target_bed.x, self.__target_bed.y, self.__target_bed.z, 0.5)
        self._bot.pathfinder.setGoal(goal)

    def update(self):
        super().update()
        if self.__target_bed.distanceTo(Vector3(self._bot.entity.position)) < 1:
            self._bot.sleep(self._bot.blockAt(Vec3(self.__target_bed.x, self.__target_bed.y, self.__target_bed.z)))

    def is_possible(self) -> bool:
        return 12541 <= self._bot.time.timeOfDay <= 23458

    def has_ended(self) -> bool:
        return (
            self._bot.isSleeping
            or (23458 <= self._bot.time.timeOfDay <= 23999)
            or (0 <= self._bot.time.timeOfDay <= 12541)
        )

    def exit(self):
        super().exit()
        self._bot.pathfinder.setGoal(None)


class WanderAroundPractice(Practice):

    __target_position: Vector3

    def __init__(self, bot, percepton: list[Perceptron]) -> None:
        super().__init__(bot, percepton, "WanderAround", 5)
        self.__target_position = None

    def setup(self):
        super().setup()
        self.__target_position = Vector3(self._bot.entity.position).add(
            Vector3(random.randrange(-5, 5), 0, random.randrange(-5, 5))
        )

    def start(self):
        super().start()

        goal = pathfinder.goals.GoalNear(
            self.__target_position.x, self.__target_position.y, self.__target_position.z, 0.5
        )
        self._bot.pathfinder.setGoal(goal)

    def update(self):
        super().update()

    def is_possible(self) -> bool:
        return True

    def has_ended(self) -> bool:
        return super().has_ended()

    def exit(self):
        super().exit()


class RandomlyLookAround(Practice):

    __target_yaw: float
    __target_pitch: float

    def __init__(self, bot, percepton: list[Perceptron]) -> None:
        super().__init__(bot, percepton, "RandomlyLookAround")

    def setup(self) -> None:
        self.__target_yaw = random.normalvariate(self._bot.entity.yaw, 3.14 / 3)
        self.__target_pitch = random.normalvariate(0, 0.3 / 2)

    def start(self) -> None:
        super().start()
        self._bot.look(self.__target_yaw, self.__target_pitch)

    def update(self) -> None:
        super().update()

    def exit(self) -> None:
        super().exit()

    def has_ended(self) -> bool:
        return True

    def is_possible(self) -> bool:
        return True


class LookToRandomPlayer(Practice):
    def __init__(self, bot, percepton: list[Perceptron]) -> None:
        super().__init__(bot, percepton, "LookToRandomPlayer", timeout=5)

    def setup(self) -> None:
        self.__target_player = self._bot.nearestEntity()

    def start(self) -> None:
        super().start()

    def update(self) -> None:
        target_position = Vector3(self.__target_player.position).add(Vector3(0, self.__target_player.height, 0))
        self._bot.lookAt(target_position.toVec3())
        super().update()

    def exit(self) -> None:
        super().exit()

    def has_ended(self) -> bool:
        return super().has_ended()

    def is_possible(self) -> bool:
        return True
