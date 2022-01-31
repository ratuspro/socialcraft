from javascript import On
from socialcraft_handler import Socialcraft_Handler
from csf import Brain, Interpreter, Perception, Context, Affordance
from csf.frames import CognitiveSocialFrame


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


class WorkweekInterpreter(Interpreter):
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


class BuilderFrame(CognitiveSocialFrame):
    def __init__(self) -> None:
        super().__init__({"WORKTIME"})

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)
        perceptions = context.get_perceptions("WORKTIME")

        if len(perceptions) == 1:
            return list(perceptions)[0].value > 0

    def get_affordances(self) -> set[Affordance]:
        return {"CAN_WORK_AS_BUILDER"}


# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

# Init CSF Brain
csf = Brain()
csf.add_interpreter(WorkweekInterpreter())
csf.add_interpreter(SocialRelationshipInterpreter())
csf.add_frame(BuilderFrame())


# Start Bot
bot = handler.bot


@On(bot, "time")
def handleTick(*args):
    csf.add_perception_to_buffer(Perception("WEEKDAY", bot.time.day % 7))
    csf.add_perception_to_buffer(Perception("TIME", bot.time.timeOfDay))

    for entity in bot.entities:
        csf.add_perception_to_buffer(Perception("PLAYER", entity))

    csf.update_saliences()

    print(csf.get_affordances())
