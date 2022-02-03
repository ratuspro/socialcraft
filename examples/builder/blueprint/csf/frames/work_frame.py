import csf.practices
from javascript import require

import csf.core
from .cognitive_social_frame import CognitiveSocialFrame

Vec3 = require("vec3")
pathfinder = require("mineflayer-pathfinder")


class WorkFrame(CognitiveSocialFrame):
    def __init__(self, bot, workplace) -> None:
        super().__init__({"WORKTIME"})
        self.__bot = bot
        self.__workplace = workplace

    def is_salient(self, context: csf.core.Context) -> bool:
        perceptions = context.get_perceptions("WORKTIME")
        return len(perceptions) == 1 and perceptions[0].value > 0

    def get_affordances(self) -> set:
        return {GoToWork(self, self.__bot, self.__workplace)}


class GoToWork(csf.practices.Practice):
    def __init__(self, creator, bot, workplace) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__workplace = workplace

    def start(self) -> None:
        if self.is_finished():
            return

        if self.__bot.entity.position.distanceTo(self.__workplace) < 1.5:
            return

        self.__bot.pathfinder.goto(
            pathfinder.goals.GoalNear(self.__workplace.x, self.__workplace.y, self.__workplace.z, 0.5),
            lambda err, result: print(result),
        )

    def exit(self) -> None:
        pass

    def is_finished(self) -> bool:
        return False
