from typing import Tuple
from javascript import On, require
from socialcraft_handler import Socialcraft_Handler
from csf import Brain, Interpreter, Perception, Context, Affordance, print_context
from csf.frames import CognitiveSocialFrame
import json
import time

pathfinder = require("mineflayer-pathfinder")
Vec3 = require("vec3")

####################
### Interpreters


class SocialRelationshipInterpreter(Interpreter):
    def __init__(self, friends: set[str] = {}, enemies: set[str] = {}) -> None:
        self.__friends = friends
        self.__enemies = enemies

    def process_perceptions(self, perceptions: Context) -> set[Perception]:
        social_labels = set()

        for perception in perceptions.get_perceptions(name="PLAYER"):
            if perception.name == "PLAYER" and perception.value in self.__friends:
                social_labels.add(Perception("FRIEND", perception.value))
            elif perception.name == "PLAYER" and perception.value in self.__enemies:
                social_labels.add(Perception("ENEMY", perception.value))
            else:
                social_labels.add(Perception("STRANGER", perception.value))

        return social_labels


class WorkTimeInterpreter(Interpreter):
    def __init__(self) -> None:
        self.__workdays = {
            Perception("WEEKDAY", 0),
            Perception("WEEKDAY", 1),
            Perception("WEEKDAY", 2),
            Perception("WEEKDAY", 3),
            Perception("WEEKDAY", 4),
        }

    def process_perceptions(self, perceptions: Context) -> set[Perception]:
        if not self.__workdays.isdisjoint(perceptions.get_perceptions("WEEKDAY")):

            time = list(perceptions.get_perceptions("TIME"))[0].value

            if time > 1500 and time < 12000:
                return {Perception("WORKTIME", 1)}

        return {Perception("WORKTIME", 0)}


class SleepInterpreter(Interpreter):
    def __init__(self, min_hour: int, max_hour: int) -> None:
        self.__sleep_interval = (min_hour, max_hour)

    def process_perceptions(self, perceptions: Context) -> set[Perception]:
        time = list(perceptions.get_perceptions("TIME"))[0].value

        if time > self.__sleep_interval[0] and time < self.__sleep_interval[1]:
            return {Perception("SLEEPTIME", 1)}

        return {Perception("SLEEPTIME", 0)}


####################
### Frames


class WorkFrame(CognitiveSocialFrame):
    def __init__(self, workplace) -> None:
        super().__init__({"WORKTIME"})
        self.__workplace = workplace

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)
        perceptions = context.get_perceptions("WORKTIME")

        print(list(perceptions)[0])
        if len(perceptions) == 1:
            return list(perceptions)[0].value > 0

    def get_affordances(self) -> set[Affordance]:
        return {Affordance("CAN_WORK", self.__workplace, 1)}


class SleepFrame(CognitiveSocialFrame):
    def __init__(self, bed_position) -> None:
        super().__init__({"SLEEPTIME"})
        self.__bed_position = bed_position

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)
        perceptions = context.get_perceptions("SLEEPTIME")

        print(str(list(perceptions)[0]))
        if len(perceptions) == 1:
            return list(perceptions)[0].value == 1

        return False

    def get_affordances(self) -> set[Affordance]:
        return {Affordance("CAN_SLEEP", self.__bed_position, 1.0)}


####################
### Practices


class GoToBed:
    def __init__(self, bot, bed_position: Vec3, needed_aff_name: str) -> None:
        self.__bot = bot
        self.__bed = bot.blockAt(bed_position)
        self.__needed_aff_name = needed_aff_name

    def has_finished(self) -> bool:
        return self.__bot.isSleeping

    def is_valid(self, affs: list[Affordance]) -> bool:
        for aff in affs:
            print(f"{aff.name}  == {self.__needed_aff_name}")
            if aff.name == self.__needed_aff_name:
                print(f"got to bed not valid anymore")
                return True
        return False

    def start(self) -> None:
        if not self.__bot.isABed(self.__bed):
            print(f"Not a bed at {self.__bed.position}")
            return

        if self.__bot.entity.position.distanceTo(self.__bed.position) < 1.5:
            self.__sleep()
            return

        self.__bot.pathfinder.goto(
            pathfinder.goals.GoalGetToBlock(self.__bed.position.x, self.__bed.position.y, self.__bed.position.z),
            lambda err, result: self.__sleep(),
        )

    def exit(self) -> None:
        if self.__bot.isSleeping:
            self.__bot.wake()

    def __sleep(self):
        self.__bot.sleep(self.__bed)


class GoToWork:
    def __init__(self, bot, workplace_position: Vec3, needed_aff_name: str) -> None:
        self.__bot = bot
        self.__workplace_pos = workplace_position
        self.__needed_aff_name = needed_aff_name

    def has_finished(self) -> bool:
        return False

    def is_valid(self, affs: list[Affordance]) -> bool:
        for aff in affs:
            print(f"{aff.name}  == {self.__needed_aff_name}")
            if aff.name == self.__needed_aff_name:
                print(f"got to work not valid anymore")
                return True
        return False

    def start(self) -> None:

        if self.__bot.entity.position.distanceTo(self.__workplace_pos) < 1.5:
            self.__bot.chat("working...")
            time.sleep(4)
            return

        self.__bot.pathfinder.goto(
            pathfinder.goals.GoalGetToBlock(self.__workplace_pos.x, self.__workplace_pos.y, self.__workplace_pos.z),
            lambda err, result: self.__work(),
        )

    def exit(self) -> None:
        if self.__bot.entity.position.distanceTo(self.__workplace_pos) < 1.5:
            self.__bot.chat("stopped working...")

    def __work(self):
        self.__bot.chat("working...")
        time.sleep(4)


# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

# Init CSF Brain
csf = Brain()
csf.add_interpreter(WorkTimeInterpreter())
csf.add_interpreter(SocialRelationshipInterpreter())
csf.add_interpreter(SleepInterpreter(16000, 23999))

if handler.has_init_env_variable("bed"):
    bed_json = json.loads(handler.get_init_env_variable("bed"))
    bed = Vec3(bed_json["x"], bed_json["y"], bed_json["z"])
    csf.add_frame(SleepFrame(bed))

if handler.has_init_env_variable("rel"):
    rel_json = json.loads(handler.get_init_env_variable("rel"))
    csf.add_interpreter(SocialRelationshipInterpreter(friends=rel_json["friends"]))

if handler.has_init_env_variable("workplace"):
    workplace_json = json.loads(handler.get_init_env_variable("workplace"))
    workplace = Vec3(workplace_json["x"], workplace_json["y"], workplace_json["z"])
    print(workplace)
    csf.add_frame(WorkFrame(workplace))

# Start Bot
bot = handler.bot

bot.onGoingPractice = None


@On(bot, "time")
def handleTick(*args):
    csf.add_perception_to_buffer(Perception("WEEKDAY", bot.time.day % 7))
    csf.add_perception_to_buffer(Perception("TIME", bot.time.timeOfDay))

    for entity in bot.entities:
        csf.add_perception_to_buffer(Perception("PLAYER", entity))

    csf.update_saliences()

    possibleActions = []

    if bot.onGoingPractice == None:
        for aff in csf.get_affordances():
            if aff.name == "CAN_SLEEP":
                possibleActions.append((GoToBed(bot, aff.value, aff.name), aff.value))

            if aff.name == "CAN_WORK":
                possibleActions.append((GoToWork(bot, aff.value, aff.name), aff.value))

        if len(possibleActions) > 0:
            possibleActions[0][0].start()
            bot.onGoingPractice = possibleActions[0]
