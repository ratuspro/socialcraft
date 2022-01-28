from javascript import On
from socialcraft_handler import Socialcraft_Handler
from csf import Brain, Interpreter, Perception, Context, Affordance
from csf.frames import CognitiveSocialFrame


class WorkweekInterpreter(Interpreter):
    def __init__(self) -> None:
        self.__workdays = {
            Perception("WEEKDAY", 0),
            Perception("WEEKDAY", 1),
            Perception("WEEKDAY", 2),
            Perception("WEEKDAY", 3),
            Perception("WEEKDAY", 4),
        }

    def process_perceptions(self, perceptions: set[Perception]) -> set[Perception]:
        if not self.__workdays.isdisjoint(perceptions):
            return {Perception("WORKDAY", 1)}
        else:
            return {Perception("WORKDAY", 0)}


class Builder(CognitiveSocialFrame):
    def __init__(self) -> None:
        super().__init__({"WORKDAY"})

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)
        perception = context.get_perception("WORKDAY")
        return perception != None and perception.value > 0

    def get_affordances(self) -> set[Affordance]:
        return {"CAN_WORK_AS_BUILDER"}


# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

bot = handler.bot

# Init CSF Brain
csf = Brain()
csf.add_interpreter(WorkweekInterpreter())
csf.add_frame(Builder())


@On(bot, "time")
def handleTick(*args):
    csf.add_perception_to_buffer(Perception("WEEKDAY", bot.time.day % 7))

    csf.update_saliences()

    print(csf.get_affordances())
