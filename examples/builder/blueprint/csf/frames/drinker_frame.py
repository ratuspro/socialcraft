import csf.practices
from javascript import require

import csf.core
from .cognitive_social_frame import CognitiveSocialFrame

Vec3 = require("vec3")
pathfinder = require("mineflayer-pathfinder")


class DrinkerFrame(CognitiveSocialFrame):
    def __init__(self, bot, bar) -> None:
        super().__init__({"PARTYTIME"})
        self.__bot = bot
        self.__bar = bar

    def get_affordances(self, context: csf.core.Context) -> set[csf.core.Affordance]:
        perceptions = context.get_perceptions("PARTYTIME")
        return {csf.core.Affordance(GoToBar(self, self.__bot, self.__bar), len(perceptions) * perceptions[0].value)}


class GoToBar(csf.practices.Practice):
    def __init__(self, creator, bot, bar) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__bar = bar

    def start(self) -> None:
        self._state = csf.practices.Practice.State.RUNNING
        if self.is_finished():
            return

        if self.__bot.entity.position.distanceTo(self.__bar) < 1.5:
            return

        self.__bot.pathfinder.goto(
            pathfinder.goals.GoalNear(self.__bar.x, self.__bar.y, self.__bar.z, 0.5),
            lambda err, result: print(err) if err is not None else print(result),
        )

    def exit(self) -> None:
        pass

    def is_finished(self) -> bool:
        return False

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, GoToBar):
            return self.__bar == __o.__bar
        return False

    def __hash__(self) -> int:
        return hash((self.__bar))
