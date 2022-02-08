import csf.practices
from javascript import require

import csf.core
import csf.practices
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
        if self.is_finished():
            self.exit()
            self.change_state(csf.practices.Practice.State.FINISHED)
            return

        if self.__bot.entity.position.distanceTo(self.__bar) < 1.5:
            self.exit()
            self.change_state(csf.practices.Practice.State.FINISHED)
            return

        self.__bot.pathfinder.setGoal(pathfinder.goals.GoalNear(self.__bar.x, self.__bar.y, self.__bar.z, 1.5))

        self.change_state(csf.practices.Practice.State.RUNNING)

    def update(self):
        bot_position = self.__bot.entity.position
        if not self.__bot.isSleeping and bot_position.distanceTo(self.__bar) < 1.5:
            self.change_state(csf.practices.Practice.State.FINISHED)
            return

    def exit(self) -> None:
        pass

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, GoToBar):
            return self.__bar == __o.__bar
        return False

    def __hash__(self) -> int:
        return hash((self.__bar))
