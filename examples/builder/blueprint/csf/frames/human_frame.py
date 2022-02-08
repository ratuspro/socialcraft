from unicodedata import name
from javascript import require, On, off

from .cognitive_social_frame import CognitiveSocialFrame
import csf.core
import csf.practices
import random


Vec3 = require("vec3")
pathfinder = require("mineflayer-pathfinder")


class HumanFrame(CognitiveSocialFrame):
    def __init__(self, bot, bed) -> None:
        super().__init__({"WORKTIME"})
        self.__bot = bot
        self.__bed = bed

    def get_affordances(self, context: csf.core.Context) -> set[csf.core.Affordance]:
        new_affordances = set()

        sleep_perception = context.get_perceptions("SLEEPTIME")
        if len(sleep_perception) == 1 and sleep_perception[0].value > 0:
            new_affordances.add(csf.core.Affordance(Sleep(self, self.__bot, self.__bed), sleep_perception[0].value))

        new_affordances.add(csf.core.Affordance(WanderAround(self, self.__bot), 0.2))

        return new_affordances


class Sleep(csf.practices.Practice):
    def __init__(self, creator, bot, bed) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__bed = bed
        self.__bed_block = self.__bot.blockAt(self.__bed)

    def start(self) -> None:
        if self.is_finished():
            return

        self.change_state(csf.practices.Practice.State.RUNNING)

        if self.__bot.isSleeping:
            return

        if self.__bot.entity.position.distanceTo(self.__bed) < 1.5 and not self.__bot.isSleeping:
            self.__sleep()
            return

        print("Setting sleeping target" + str(self.__bed))
        self.__bot.pathfinder.setGoal(
            pathfinder.goals.GoalGetToBlock(self.__bed.x, self.__bed.y, self.__bed.z),
        )

    def update(self):
        bot_position = self.__bot.entity.position
        if not self.__bot.isSleeping and bot_position.distanceTo(self.__bed) < 1.5:
            self.__sleep()
            return

    def exit(self) -> None:
        if self.__bot.isSleeping:
            self.__bot.wake(self.__on_awake)

    def __on_awake(arg1, arg2, arg3):
        print(arg1)
        print(arg2)
        print(arg3)

    def __sleep(self):
        self.__bot.sleep(self.__bed_block)

    def is_finished(self) -> bool:
        return False

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Sleep):
            return self.__bed == __o.__bed
        return False

    def __hash__(self) -> int:
        return hash((self.__bed))


class WanderAround(csf.practices.Practice):
    def __init__(self, creator, bot) -> None:
        super().__init__(creator)
        self.__bot = bot
        curr_position = self.__bot.entity.position

        self.__target_position = Vec3(
            curr_position.x + random.randrange(-8, 8), curr_position.y, curr_position.z + random.randrange(-8, 8)
        )

    def start(self) -> None:
        self._state = csf.practices.Practice.State.RUNNING
        if self.is_finished():
            return

        bot_position = self.__bot.entity.position
        if bot_position.distanceTo(self.__target_position) < 1.5:
            return

        self.__bot.pathfinder.setGoal(
            pathfinder.goals.GoalNearXZ(self.__target_position.x, self.__target_position.z, 1.5)
        )

        self.change_state(csf.practices.Practice.State.RUNNING)

    def update(self):
        bot_position = self.__bot.entity.position
        if bot_position.distanceTo(self.__target_position) < 1.5:
            self.change_state(csf.practices.Practice.State.FINISHED)
            return

    def exit(self) -> None:
        pass

    def is_finished(self) -> bool:
        print(self.__bot.isMoving)
        return self.state == csf.practices.Practice.State.FINISHED

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, WanderAround):
            return True
        return False

    def __hash__(self) -> int:
        return hash(0)
