import json
import logging
import sys
from datetime import datetime
from javascript import On, require, start, AsyncTask, stop, eval_js
from socialcraft_handler import Socialcraft_Handler

from csf import Brain, print_context
from csf.frames import WorkFrame, HumanFrame, DrinkerFrame, BardFrame
from csf.interpreters import SocialRelationshipInterpreter, WorkTimeInterpreter, SleepInterpreter, PartyTimeInterpreter
from csf.core import Perception
from csf.practices import Practice

Vec3 = require("vec3")

# Init Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

# Init CSF Brain
csf = Brain()
csf.add_interpreter(WorkTimeInterpreter())

friends = []
if handler.has_init_env_variable("friends"):
    friends.extend(json.loads(handler.get_init_env_variable("friends")))


csf.add_interpreter(SocialRelationshipInterpreter(friends))
csf.add_interpreter(SleepInterpreter(16000, 23999))
csf.add_interpreter(PartyTimeInterpreter())
# Start Bot
bot = handler.bot
if handler.has_init_env_variable("workplace"):
    position_json = json.loads(handler.get_init_env_variable("workplace"))
    workplace = Vec3(position_json["x"], position_json["y"], position_json["z"])
    csf.add_frame(WorkFrame(bot, workplace))
else:
    csf.add_frame(BardFrame(bot))

if handler.has_init_env_variable("bed"):
    bed_json = json.loads(handler.get_init_env_variable("bed"))
    bed = Vec3(bed_json["x"], bed_json["y"], bed_json["z"])
    csf.add_frame(HumanFrame(bot, bed))

if handler.has_init_env_variable("bar"):
    bar_json = json.loads(handler.get_init_env_variable("bar"))
    bar = Vec3(bar_json["x"], bar_json["y"], bar_json["z"])
    csf.add_frame(DrinkerFrame(bot, bar))

bot.available_affordances = []
bot.active_affordance = None
bot.last_update = bot.time.time


@AsyncTask(start=True)
def async_perceive_work(task):
    while not task.stopping:

        logger.info(f"Start Perceiving World at {bot.time.time}")
        start_time = datetime.now()
        csf.add_perception_to_buffer(Perception("WEEKDAY", bot.time.day % 7))
        csf.add_perception_to_buffer(Perception("TIME", bot.time.timeOfDay))

        bot_position = bot.entity.position

        for entity in bot.entities:
            if int(entity) != int(bot.entity.id):
                other_position = bot.entities[entity].position
                if other_position.distanceTo(bot_position) < 10:
                    csf.add_perception_to_buffer(Perception("PLAYER", entity))
        logger.debug(f"World perceived!")

        logger.debug(f"Updating saliences...")
        csf.update_saliences()
        logger.debug(f"Saliences updated...")

        logger.debug(f"Determine Best Affordance...")
        available_affordances = csf.get_affordances()
        available_affordances.sort(key=lambda x: x.salience, reverse=True)

        if len(available_affordances) == 0:
            logger.debug(f"No new affordances available!")
        else:
            logger.debug(f"New affordances available:")
            for i in range(0, len(available_affordances)):
                logger.debug(f"[{i}] {available_affordances[i]}")

        if bot.active_affordance is not None:
            logger.debug(f"Previous Affordance: ")
            logger.debug(f"{bot.active_affordance}")

            valid_practice = bot.active_affordance.object.is_valid(csf.get_last_context())
            finished_practice = bot.active_affordance.object.is_finished()
            another_practice_more_salient = (
                len(available_affordances) > 0 and available_affordances[0].salience > bot.active_affordance.salience
            )

            logger.debug(f"[{ 'X' if valid_practice else ' '}] Still Valid.")
            logger.debug(f"[{ 'X' if not finished_practice else ' '}] Ongoing.")
            logger.debug(f"[{ 'X' if not another_practice_more_salient else ' '}] Highest salience.")

            if not valid_practice or finished_practice or another_practice_more_salient:
                logger.debug("Stopping previous affordance...")
                logger.debug(bot.active_affordance.object)

                bot.active_affordance.object.exit()
                bot.active_affordance = None
                logger.debug("Previous affordance stopped.")
            else:
                logger.debug("Maintain previous affordance.")
        else:
            logger.debug(f"No previous Affordanced deployed ")

        if bot.active_affordance is None and len(available_affordances) > 0:
            logger.debug(f"Deploying new affordance:")
            logger.debug(f"{available_affordances[0]}")
            bot.active_affordance = available_affordances[0]
            logger.debug(f"Affordance deployed!")
            bot.active_affordance.object.start()

        time_spent = datetime.now() - start_time
        logger.info(
            f"Affordances updated after {(time_spent.days * 24 * 60 * 60 + time_spent.seconds) * 1000 + time_spent.microseconds / 1000.0} miliseconds"
        )
        task.wait(2)


@On(bot, "time")
def handleTick(_):

    if abs(bot.time.time - bot.last_update) < 200:
        return
    else:
        bot.last_update = bot.time.time

    logger.info(f"Start new update at {bot.time.time}")
    start_time = datetime.now()

    if bot.active_affordance.object.state == Practice.State.CREATED:
        bot.active_affordance.object.start()

    if bot.active_affordance.object.state == Practice.State.RUNNING:
        bot.active_affordance.object.update()

    time_spent = datetime.now() - start_time
    logger.info(
        f"Last update took {(time_spent.days * 24 * 60 * 60 + time_spent.seconds) * 1000 + time_spent.microseconds / 1000.0} miliseconds"
    )
