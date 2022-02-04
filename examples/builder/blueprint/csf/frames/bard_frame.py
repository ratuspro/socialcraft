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

    def is_salient(self, context: csf.core.Context) -> bool:
        perceptions = context.get_perceptions("PLAYER")
        for perception in perceptions:
            self.__players.append(perception.value)
        return len(perceptions) > 1

    def get_affordances(self) -> set:
        return {csf.core.Affordance(TalkAbout(self, self.__bot, random.choice(self.__players)), 0.9)}


class TalkAbout(csf.practices.Practice):
    def __init__(self, creator, bot, target) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__player = bot.entities[target]
        self.__finished = False

    def start(self) -> None:
        print("Starting practice...")
        print(f"player: {self.__player.username}")
        if self.is_finished():
            return

        if self.__player is None:
            self.__finished = True
            return

        if self.__bot.entity.position.distanceTo(self.__player.position) < 3:
            print("Already close to the target.")
            self.__talk_about()
            return

        print(f"{self.__bot.pathfinder} moving from")
        print(f"{self.__bot.entity.position}")
        print(f"towards {self.__player.position}.")
        self.__bot.pathfinder.setGoal(
            pathfinder.goals.GoalNear(self.__player.position.x, self.__player.position.y, self.__player.position.z, 3)
        )

        @On(self.__bot, "goal_reached")
        def handle_arrival(arg1, arg2):
            off(self.__bot, "goal_reached", handle_arrival)
            self.__talk_about()

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
