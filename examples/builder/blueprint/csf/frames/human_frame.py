from javascript import require

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

    def is_salient(self, context: csf.core.Context) -> bool:
        return True

    def get_affordances(self) -> set:
        return {
            csf.core.Affordance(Sleep(self, self.__bot, self.__bed), 0.2),
            csf.core.Affordance(WanderAround(self, self.__bot), 0.4),
        }


class Sleep(csf.practices.Practice):
    def __init__(self, creator, bot, bed) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__bed = bed
        self.__bed_block = self.__bot.blockAt(self.__bed)

    def start(self) -> None:
        print("starting sleep")

        if self.is_finished():
            return

        if self.__bot.entity.position.distanceTo(self.__bed) < 1.5:
            self.__sleep()
            return

        print("Setting sleeping target" + str(self.__bed))
        self.__bot.pathfinder.goto(
            pathfinder.goals.GoalGetToBlock(self.__bed.x, self.__bed.y, self.__bed.z),
            lambda err, result: self.__sleep(),
        )

    def exit(self) -> None:
        if self.__bot.isSleeping:
            self.__bot.wake(self.__on_awake)

    def __on_awake(err, result):
        print(err)
        print(result)

    def __sleep(self):
        self.__bot.sleep(self.__bed_block)

    def is_finished(self) -> bool:
        return False


class WanderAround(csf.practices.Practice):
    def __init__(self, creator, bot) -> None:
        super().__init__(creator)
        self.__bot = bot
        curr_position = self.__bot.entity.position

        self.__target_position = Vec3(
            curr_position.x + random.randrange(-8, 8), 0, curr_position.z + random.randrange(-8, 8)
        )

    def start(self) -> None:
        if self.is_finished():
            return

        bot_position = self.__bot.entity.position
        if bot_position.distanceTo(self.__target_position) < 1.5:
            return

        self.__bot.pathfinder.setGoal(
            pathfinder.goals.GoalNearXZ(self.__target_position.x, self.__target_position.z, 1)
        )

    def exit(self) -> None:
        self.__bot.pathfinder.stop()

    def is_finished(self) -> bool:
        if self.__bot.entity.position.distanceTo(self.__target_position) < 1.5:
            return True
        return False
