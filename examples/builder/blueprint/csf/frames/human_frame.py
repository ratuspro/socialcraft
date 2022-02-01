from javascript import require

from .cognitive_social_frame import CognitiveSocialFrame
import csf.core
import csf.practices


Vec3 = require("vec3")
pathfinder = require("mineflayer-pathfinder")


class HumanFrame(CognitiveSocialFrame):
    def __init__(self, bot, bed) -> None:
        super().__init__({"WORKTIME"})
        self.__bot = bot
        self.__bed = bed

    def is_salient(self, context: csf.core.Context) -> bool:
        perceptions = context.get_perceptions("SLEEPTIME")
        return len(perceptions) == 1 and perceptions[0].value > 0

    def get_affordances(self) -> set:
        return {Sleep(self, self.__bot, self.__bed)}


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
