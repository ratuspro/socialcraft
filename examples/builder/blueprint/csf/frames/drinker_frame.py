import csf.practices
from javascript import require

import csf.core
from .cognitive_social_frame import CognitiveSocialFrame

Vec3 = require("vec3")
pathfinder = require("mineflayer-pathfinder")


class DrinkerFrame(CognitiveSocialFrame):
    def __init__(self, bot, bar) -> None:
        super().__init__({"WORKTIME"})
        self.__bot = bot
        self.__bar = bar

    def is_salient(self, context: csf.core.Context) -> bool:
        perceptions = context.get_perceptions("WORKTIME")
        return len(perceptions) == 1 and perceptions[0].value == 0

    def get_affordances(self) -> set:
        return {GoToBar(self, self.__bot, self.__bar)}


class GoToBar(csf.practices.Practice):
    def __init__(self, creator, bot, bar) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__bar = bar

    def start(self) -> None:
        if self.is_finished():
            return

        self.__bot.pathfinder.goto(
            pathfinder.goals.GoalNear(self.__bar.x, self.__bar.y, self.__bar.z, 0.5),
            lambda err, result: print(str(err) + str(result)),
        )

    def exit(self) -> None:
        pass

    def is_finished(self) -> bool:
        return False
