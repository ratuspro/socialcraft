from typing import Tuple
from javascript import On, require
from socialcraft_handler import Socialcraft_Handler
from csf import Brain, Interpreter, Perception, Context, Affordance, print_context
from csf.frames import CognitiveSocialFrame

pathfinder = require("mineflayer-pathfinder")
Vec3 = require("vec3")


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


class BuilderFrame(CognitiveSocialFrame):
    def __init__(self) -> None:
        super().__init__({"WORKTIME"})

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)
        perceptions = context.get_perceptions("WORKTIME")

        if len(perceptions) == 1:
            return list(perceptions)[0].value > 0

    def get_affordances(self) -> set[Affordance]:
        return {Affordance("CAN_WORK_AS_BUILDER", True, 1)}


class SleepFrame(CognitiveSocialFrame):
    def __init__(self) -> None:
        super().__init__({"SLEEPTIME"})

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)
        perceptions = context.get_perceptions("SLEEPTIME")

        print(str(list(perceptions)[0]))
        if len(perceptions) == 1:
            return list(perceptions)[0].value == 1

        return False

    def get_affordances(self) -> set[Affordance]:
        return {Affordance("CAN_SLEEP", None, 1.0)}


class GoToBed:
    def __init__(self, bot, bed_position: Vec3) -> None:
        self.__bot = bot
        self.__bed = bot.blockAt(bed_position)

    def has_finished(self) -> bool:
        return self.__bot.isSleeping

    def is_valid(self) -> bool:
        return True

    def start(self) -> None:
        if not self.__bot.isABed(self.__bed):
            print(f"Not a bed at {self.__bed.position}")
            return

        if self.__bot.entity.position.distanceTo(self.__bed.position) < 1.5:
            self.__sleep()
            return

        bot.pathfinder.goto(
            pathfinder.goals.GoalGetToBlock(self.__bed.position.x, self.__bed.position.y, self.__bed.position.z),
            lambda err, result: self.__sleep(),
        )

    def __sleep(self):
        self.__bot.sleep(self.__bed)


# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

# Init CSF Brain
csf = Brain()
csf.add_interpreter(WorkTimeInterpreter())
csf.add_interpreter(SocialRelationshipInterpreter())
csf.add_interpreter(SleepInterpreter(16000, 23999))
csf.add_frame(BuilderFrame())
csf.add_frame(SleepFrame())


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

    print("Affordances: ")
    possibleActions = []

    if bot.onGoingPractice == None:
        for aff in csf.get_affordances():
            if aff.name == "CAN_SLEEP":
                possibleActions.append((GoToBed(bot, Vec3(19, 4, 22)), aff.value))

        if len(possibleActions) > 0:
            possibleActions[0][0].start()

        bot.onGoingPractice = possibleActions[0]
