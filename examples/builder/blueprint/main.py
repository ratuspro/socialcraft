import json
import random
from javascript import On, require
from socialcraft_handler import Socialcraft_Handler

from csf import Brain, print_context
from csf.frames import WorkFrame, HumanFrame, DrinkerFrame
from csf.interpreters import SocialRelationshipInterpreter, WorkTimeInterpreter, SleepInterpreter, PartyTimeInterpreter
from csf.core import Perception, Affordance

Vec3 = require("vec3")

# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

# Init CSF Brain
csf = Brain()
csf.add_interpreter(WorkTimeInterpreter())

friends = []
if handler.has_init_env_variable("friends"):
    friends.extend(json.loads(handler.get_init_env_variable("friends")))
print(friends)


csf.add_interpreter(SocialRelationshipInterpreter(friends))
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


bot.active_affordance = None


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
    affordances.sort(key=lambda x: x.salience, reverse=True)

    if bot.active_affordance is not None:
        print("## Previous Practice: ")
        print(bot.active_affordance)

        valid_practice = bot.active_affordance.object.is_valid(csf.get_last_context())
        finished_practice = bot.active_affordance.object.is_finished()
        another_practice_more_salient = (
            len(affordances) > 0 and affordances[0].salience > bot.active_affordance.salience
        )

        print("   = " + ("Practice still valid" if valid_practice else "Practice not valid"))
        print("   = " + ("Practice finished" if finished_practice else "Practice not yet finished"))
        print(
            "   = "
            + ("Not the most salient frame" if another_practice_more_salient else "Still is the most salient frame")
        )

        if not valid_practice or finished_practice or another_practice_more_salient:
            print("On going practice not adequate anymore. Deleting practice...")
            print(bot.active_affordance.object)

            bot.active_affordance.object.exit()
            bot.active_affordance = None

    if bot.active_affordance is None and len(affordances) > 0:
        print("## New Practices Available!")
        for new_practice in affordances:
            print("    = " + str(new_practice))

        bot.active_affordance = affordances[0]

        print("### Selected practice:")
        print(bot.active_affordance)
        bot.active_affordance.object.start()
