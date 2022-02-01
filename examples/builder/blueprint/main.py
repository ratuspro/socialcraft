import json
import random
from javascript import On, require
from socialcraft_handler import Socialcraft_Handler

from csf import Brain, print_context
from csf.frames import WorkFrame, HumanFrame
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

if handler.has_init_env_variable("workplace"):
    position_json = json.loads(handler.get_init_env_variable("workplace"))
    workplace = Vec3(position_json["x"], position_json["y"], position_json["z"])
    csf.add_frame(WorkFrame(bot, workplace))

if handler.has_init_env_variable("bed"):
    bed_json = json.loads(handler.get_init_env_variable("bed"))
    bed = Vec3(bed_json["x"], bed_json["y"], bed_json["z"])
    csf.add_frame(HumanFrame(bot, bed))


def perceive_world(bot, csf: Brain):
    csf.add_perception_to_buffer(Perception("WEEKDAY", bot.time.day % 7))
    csf.add_perception_to_buffer(Perception("TIME", bot.time.timeOfDay))

    for entity in bot.entities:
        csf.add_perception_to_buffer(Perception("PLAYER", entity))


bot.ongoing_practice = None


@On(bot, "time")
def handleTick(_):

    perceive_world(bot, csf)

    csf.update_saliences()
    affordances = csf.get_affordances()

    print(bot.ongoing_practice)

    print(affordances)
    if bot.ongoing_practice is not None:
        if not bot.ongoing_practice.is_valid(csf.get_last_context()) or bot.ongoing_practice.is_finished():
            bot.ongoing_practice.exit()
            bot.ongoing_practice = None

    if bot.ongoing_practice is None and len(affordances) > 0:

        bot.ongoing_practice = random.choice(affordances)
        print("setting affordance")
        print(bot.ongoing_practice)
        bot.ongoing_practice.start()
