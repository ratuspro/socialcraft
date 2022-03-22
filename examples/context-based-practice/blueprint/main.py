from abc import abstractclassmethod, abstractmethod
import json
import logging
import sys
import math
import random
from datetime import datetime
from typing import Dict, Tuple
from javascript import On, require, start, AsyncTask, stop, eval_js
from socialcraft_handler import Socialcraft_Handler
from vector3 import Vector3
from practices import (
    AvoidPeoplePractice,
    GoToHousePractice,
    Perceptron,
    SleepPractice,
    WanderAroundPractice,
    RandomlyLookAround,
    LookToRandomPlayer,
    ChoopWood,
    Context,
)

from perceptions import Perception, perceive_blocks, perceive_players, perceive_world_state
from perceptions.interpreters.block import BlockInterpreterManager, IsBlockCloseBy
from perceptions.interpreters.people import PeopleInterpreterManager, PeopleCloseBy


def ConvertToDirection(yaw, pitch):
    return Vector3(
        -math.sin(yaw) * math.cos(pitch),
        math.sin(bot.entity.pitch),
        -math.cos(yaw) * math.cos(pitch),
    )


# Init Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configuration
Update_Min_Time = 2500

# Init Socialcraft Handler
handler = Socialcraft_Handler()
handler.connect()

bot = handler.bot

practices = []
bot.kb = {}

if handler.has_init_env_variable("bed"):
    bed_json = json.loads(handler.get_init_env_variable("bed"))
    bot.kb["bed_position"] = Vector3(bed_json["x"], bed_json["y"], bed_json["z"])
    practices.append(
        GoToHousePractice(
            bot,
            [Perceptron("ISNIGHT", 1, 0)],
        )
    )

    practices.append(
        SleepPractice(
            bot,
            [Perceptron("ISNIGHT", 3, 0), Perceptron("OWNBEDVISIBLE", 0.6, 0)],
        )
    )

practices.append(
    AvoidPeoplePractice(
        bot,
        [],
    )
)

practices.append(
    WanderAroundPractice(
        bot,
        [Perceptron("ISDAY", 1, 0)],
    )
)

practices.append(
    RandomlyLookAround(
        bot,
        [Perceptron("ISNIGHT", 0, 0.5)],
    )
)

practices.append(
    LookToRandomPlayer(
        bot,
        [Perceptron("ISNIGHT", 0, 0.5)],
    )
)

practices.append(
    ChoopWood(
        bot,
        [Perceptron("ISDAY", 0.5, 0), Perceptron("ISNIGHT", -1, 0), Perceptron("WOOD_CLOSE_BY", 2, 0)],
    )
)

p_interpreter_manager = PeopleInterpreterManager(bot)
p_interpreter_manager.add_interpreter(PeopleCloseBy(5, "PLAYER_VERY_CLOSE"))
p_interpreter_manager.add_interpreter(PeopleCloseBy(10, "PLAYER_CLOSE"))
p_interpreter_manager.add_interpreter(PeopleCloseBy(20, "PLAYER_FAR"))

b_interpreter_manager = BlockInterpreterManager(bot)
b_interpreter_manager.add_interpreter(IsBlockCloseBy("WOOD_CLOSE_BY", ["Oak Log"]))
b_interpreter_manager.add_interpreter(IsBlockCloseBy("BED_CLOSE_BY", ["Red Bed"]))


@AsyncTask(start=True)
def async_basic_agent_loop(task):

    ongoing_practice = None

    while not task.stopping:

        logger.info("🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹")
        logger.info(f"Start Agent Loop at {bot.time.time}")
        start_time = datetime.now()

        # Create Context
        context = Context()

        # Perceive Blocks
        p_start_time = datetime.now()
        blocks_by_position = perceive_blocks(bot)
        p_delta = datetime.now() - p_start_time
        p_milliseconds = (p_delta.days * 24 * 60 * 60 + p_delta.seconds) * 1000 + p_delta.microseconds / 1000.0
        logger.debug(f"Perceiving blocks took {p_milliseconds} miliseconds")

        # Perceive People
        p_start_time = datetime.now()
        players = perceive_players(bot)
        p_delta = datetime.now() - p_start_time
        p_milliseconds = (p_delta.days * 24 * 60 * 60 + p_delta.seconds) * 1000 + p_delta.microseconds / 1000.0
        logger.debug(f"Perceiving players took {p_milliseconds} miliseconds")

        # Perceive Time
        p_start_time = datetime.now()
        world_state = perceive_world_state(bot)
        for state in world_state:
            context.add_perception(state)
        p_delta = datetime.now() - p_start_time
        p_milliseconds = (p_delta.days * 24 * 60 * 60 + p_delta.seconds) * 1000 + p_delta.microseconds / 1000.0
        logger.debug(f"Perceiving time and weather took {p_milliseconds} miliseconds")

        # Interpret Blocks
        p_start_time = datetime.now()
        blocks = list(blocks_by_position.values())
        block_interpretations = b_interpreter_manager.process(blocks)
        for interpretation in block_interpretations:
            context.add_perception(interpretation)
        for block in blocks:
            context.add_block_perception(Perception("BLOCK", 1, block))
        p_delta = datetime.now() - p_start_time
        p_milliseconds = (p_delta.days * 24 * 60 * 60 + p_delta.seconds) * 1000 + p_delta.microseconds / 1000.0
        logger.debug(f"Interpreting blocks took {p_milliseconds} miliseconds")

        # Interpret People
        p_start_time = datetime.now()
        player_interpretations = p_interpreter_manager.process(players)
        for interpretation in player_interpretations:
            context.add_perception(interpretation)
        for player in players:
            context.add_perception(Perception("PLAYER", 1, player))
        p_delta = datetime.now() - p_start_time
        p_milliseconds = (p_delta.days * 24 * 60 * 60 + p_delta.seconds) * 1000 + p_delta.microseconds / 1000.0
        logger.debug(f"Interpreting people took {p_milliseconds} miliseconds")

        all_perceptions = context.get_perceptions()
        for perception in all_perceptions:
            logger.debug(perception)

        # Update Practices Saliences
        for practice in practices:
            practice.update_salience(context)

        random.shuffle(practices)
        practices.sort(reverse=True, key=lambda practice: practice.salience)

        for practice in practices:
            logger.debug("{:<30} {:<5}".format(practice.name, practice.salience))

        # Update Ongoing Practice
        if ongoing_practice is not None:
            if not ongoing_practice.is_possible() or ongoing_practice.has_ended():
                logger.info(f"🛑 Exit Practice {ongoing_practice}")
                ongoing_practice.exit()
                ongoing_practice = None
            else:
                logger.info(f"🔃 Update Practice {ongoing_practice}")
                ongoing_practice.update()
        else:
            if practices[0].salience > 0:
                ongoing_practice = practices[0]
                logger.info(f"🚀 Start Practice {ongoing_practice}")
                ongoing_practice.setup(context)
                if ongoing_practice.is_possible():
                    ongoing_practice.start()
            else:
                logger.info("⭕ Do nothing")

        time_spent = datetime.now() - start_time
        milliseconds = (time_spent.days * 24 * 60 * 60 + time_spent.seconds) * 1000 + time_spent.microseconds / 1000.0
        logger.info(f"Last update took {milliseconds} miliseconds")

        if milliseconds < Update_Min_Time:
            time_to_wait = Update_Min_Time - int(milliseconds)
            logger.info(f"Waiting {time_to_wait} miliseconds")
            task.wait(time_to_wait / 1000)
        else:
            logger.info(f"Not waiting!")


@On(bot, "time")
def handleTick(_):
    pass
