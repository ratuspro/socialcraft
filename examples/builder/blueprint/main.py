from javascript import On, require
from socialcraft_handler import Socialcraft_Handler

from csf import Brain, print_context
from csf.interpreters import SocialRelationshipInterpreter, WorkTimeInterpreter, SleepInterpreter
from csf.core import Perception

Vec3 = require("vec3")

# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

# Init CSF Brain
csf = Brain()
csf.add_interpreter(WorkTimeInterpreter())
csf.add_interpreter(SocialRelationshipInterpreter())
csf.add_interpreter(SleepInterpreter(16000, 23999))

# Start Bot
bot = handler.bot

bot.onGoingPractice = None


def perceive_world(bot, csf: Brain):
    csf.add_perception_to_buffer(Perception("WEEKDAY", bot.time.day % 7))
    csf.add_perception_to_buffer(Perception("TIME", bot.time.timeOfDay))

    for entity in bot.entities:
        csf.add_perception_to_buffer(Perception("PLAYER", entity))


@On(bot, "time")
def handleTick(_):

    perceive_world(bot, csf)

    csf.update_saliences()

    print_context(csf.get_last_context())
