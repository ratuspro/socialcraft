import json
import random
from javascript import On, require
from socialcraft_handler import Socialcraft_Handler

from csf import Brain, print_context
from csf.frames import WorkFrame, HumanFrame, DrinkerFrame
from csf.interpreters import SocialRelationshipInterpreter, WorkTimeInterpreter, SleepInterpreter, PartyTimeInterpreter
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
csf.add_interpreter(PartyTimeInterpreter())
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

if handler.has_init_env_variable("bar"):
    bar_json = json.loads(handler.get_init_env_variable("bar"))
    bar = Vec3(bar_json["x"], bar_json["y"], bar_json["z"])
    csf.add_frame(DrinkerFrame(bot, bar))


def perceive_world(bot, csf: Brain):
    csf.add_perception_to_buffer(Perception("WEEKDAY", bot.time.day % 7))
    csf.add_perception_to_buffer(Perception("TIME", bot.time.timeOfDay))

    for entity in bot.entities:
        csf.add_perception_to_buffer(Perception("PLAYER", entity))


bot.ongoing_practice = None


bot.last_update = bot.time.time


@On(bot, "time")
def handleTick(_):

    if abs(bot.time.time - bot.last_update) < 100:
        return
    else:
        bot.last_update = bot.time.time
        print("# New tick")

    perceive_world(bot, csf)

    csf.update_saliences()

    print("## New Context: ")
    print_context(csf.get_last_context())

    affordances = csf.get_affordances()

    if bot.ongoing_practice is not None:
        print("## Previous Practice: ")
        print(bot.ongoing_practice)

        valid_practice = bot.ongoing_practice.is_valid(csf.get_last_context())
        finished_practice = bot.ongoing_practice.is_finished()

        print("   = " + "Practice still valid" if valid_practice else "Practice not valid")
        print("   = " + "Practice finished" if finished_practice else "Practice not yet finished")

        if not valid_practice or finished_practice:
            print("On going practice not adequate anymore. Deleting practice...")
            print(bot.ongoing_practice)

            bot.ongoing_practice.exit()
            bot.ongoing_practice = None

    if bot.ongoing_practice is None and len(affordances) > 0:
        print("## New Practices Available!")
        for new_practice in affordances:
            print("    = " + str(new_practice))

        bot.ongoing_practice = random.choice(affordances)

        print("### Selected practice:")
        print(bot.ongoing_practice)
        bot.ongoing_practice.start()
