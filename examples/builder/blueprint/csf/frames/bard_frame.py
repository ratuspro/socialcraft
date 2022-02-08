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
        self.change_state(csf.practices.Practice.State.RUNNING)

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

    def update(self):
        bot_position = self.__bot.entity.position
        if not self.__bot.isSleeping and bot_position.distanceTo(self.position) < 1.5:
            self.__talk_about()
            return

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
