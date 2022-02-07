import logging
import csf.practices
from javascript import require, off, On
import random

import csf.core
from .cognitive_social_frame import CognitiveSocialFrame

Vec3 = require("vec3")
pathfinder = require("mineflayer-pathfinder")


class BardFrame(CognitiveSocialFrame):
    def __init__(self, bot) -> None:
        super().__init__({"WORKTIME"})
        self.__bot = bot
        self.__players = []

    def get_affordances(self, context: csf.core.Context) -> set[csf.core.Affordance]:
        perceptions = context.get_perceptions("PLAYER")
        for perception in perceptions:
            self.__players.append(perception.value)
        return {csf.core.Affordance(TalkAbout(self, self.__bot, random.choice(self.__players)), 0.9)}


class TalkAbout(csf.practices.Practice):
    def __init__(self, creator, bot, target) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__target = target
        self.__player = bot.entities[target]
        self.__finished = False

    def start(self) -> None:
        self._state = csf.practices.Practice.State.RUNNING
        if self.is_finished():
            return

        if self.__player is None:
            self.__finished = True
            return

        if self.__bot.entity.position.distanceTo(self.__player.position) < 3:
            print("Already close to the target.")
            self.__talk_about()
            return

        goal = pathfinder.goals.GoalNear(
            self.__player.position.x, self.__player.position.y, self.__player.position.z, 3
        )

        bot_pathfinder = self.__bot.pathfinder
        bot_pathfinder.setGoal(goal)

        @On(self.__bot, "goal_reached")
        def handle_arrival(arg1, arg2):
            off(self.__bot, "goal_reached", handle_arrival)
            self.__talk_about()

        @On(self.__bot, "path_update")
        def handle_path_update(arg1, arg2):
            print("path_update")

        @On(self.__bot, "goal_updated")
        def handle_goal_updated(arg1, arg2, arg3):
            print("goal_updated")

        @On(self.__bot, "path_reset")
        def handle_path_reset(arg1, arg2):
            print("path_reset")

        @On(self.__bot, "path_stop")
        def handle_path_stop(arg1, arg2):
            print("path_stop")

    def __talk_about(self):
        self.__bot.lookAt(self.__player.position)
        self.__bot.chat(f"Another day we see {self.__player.username}")
        self.__finished = True

    def exit(self) -> None:

        pass

    def is_finished(self) -> bool:
        if self.__player is None:
            return True

        return self.__finished

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, TalkAbout):
            return self.__target == __o.__target
        return False

    def __hash__(self) -> int:
        return hash((self.__target))
