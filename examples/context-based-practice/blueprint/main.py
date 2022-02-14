from abc import abstractclassmethod, abstractmethod
import json
import logging
import sys
import math
import random
from datetime import datetime
from javascript import On, require, start, AsyncTask, stop, eval_js
from socialcraft_handler import Socialcraft_Handler
from vector3 import Vector3
from practices import (
    AvoidPeoplePractice,
    GoToHousePractice,
    Perceptron,
    PerceptionLabel,
    SleepPractice,
    WanderAroundPractice,
    RandomlyLookAround,
    LookToRandomPlayer,
    ChoopWood,
)


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
            [Perceptron(PerceptionLabel.ISNIGHT, 1, 0)],
        )
    )

    practices.append(
        SleepPractice(
            bot,
            [Perceptron(PerceptionLabel.ISNIGHT, 0.6, 0), Perceptron(PerceptionLabel.OWNBEDVISIBLE, 0.6, 0)],
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
        [Perceptron(PerceptionLabel.ISDAY, 1, 0)],
    )
)

practices.append(
    RandomlyLookAround(
        bot,
        [Perceptron(PerceptionLabel.ISNIGHT, 0, 0.5)],
    )
)

practices.append(
    LookToRandomPlayer(
        bot,
        [Perceptron(PerceptionLabel.ISNIGHT, 0, 0.5)],
    )
)

practices.append(
    ChoopWood(
        bot,
        [Perceptron(PerceptionLabel.ISDAY, 0.5, 0), Perceptron(PerceptionLabel.WOODINSIGHT, 1, 0)],
    )
)


def perceive_blocks():
    bot_head_position = Vector3(bot.entity.position).add(Vector3(0, bot.entity.height, 0))
    h_vec3 = bot_head_position.toVec3()

    min_pitch = -6
    max_pitch = 6
    min_yaw = -4
    max_yaw = 4

    pitchs = []
    yaws = []
    for pitch_increment in range(min_pitch, max_pitch + 1):
        pitch = float(bot.entity.pitch + pitch_increment * 0.125)
        pitchs.append(math.sin(pitch))

    for yaw_increment in range(min_yaw, max_yaw + 1):
        yaw = float(bot.entity.yaw + yaw_increment * 0.125)
        yaws.append((-math.sin(yaw), -math.cos(yaw)))

    blocks_position = {}
    blocks_by_type = {}

    for pitch in pitchs:
        for yaw in yaws:
            bot_facing_direction = Vector3(yaw[0], pitch, yaw[1])
            d_vec3 = bot_facing_direction.normalize().toVec3()
            block = bot.world.raycast(h_vec3, d_vec3, 15)

            if block is not None:
                block_position = Vector3(block.position)
                if block_position not in blocks_position:
                    blocks_position[block_position] = block.displayName
                    if block.displayName not in blocks_by_type:
                        blocks_by_type[block.displayName] = []
                    blocks_by_type[block.displayName].append(block_position)

    return blocks_position, blocks_by_type


def perceive_players():
    players = {}

    bot_position = Vector3(bot.entity.position)

    for player in bot.players:

        if player == bot.username:
            continue

        player_entity = bot.players[player].entity
        if player_entity is not None:
            player_pos = Vector3(player_entity.position)
            if bot_position.xzDistanceTo(player_pos) < 20:
                players[player_pos] = player

    return players


@AsyncTask(start=True)
def async_basic_agent_loop(task):

    ongoing_practice = None

    while not task.stopping:

        logger.info(f"Start Agent Loop at {bot.time.time}")
        start_time = datetime.now()

        blocks_by_position, blocks_by_type = perceive_blocks()
        players = perceive_players()

        # Perceive
        perceptions = {}
        perceptions[PerceptionLabel.TIME] = bot.time.timeOfDay / 24000
        perceptions[PerceptionLabel.ISDAY] = 1 if bot.time.isDay else 0
        perceptions[PerceptionLabel.ISNIGHT] = 1 if not bot.time.isDay else 0
        perceptions[PerceptionLabel.WEEKDAY] = bot.time.day % 7
        perceptions[PerceptionLabel.RAIN] = bot.rainState
        perceptions[PerceptionLabel.THUNDER] = bot.thunderState

        perceptions[PerceptionLabel.OWNBEDVISIBLE] = 0
        if "Red Bed" in blocks_by_type and bot.kb["bed_position"] is not None:
            for position in blocks_by_type["Red Bed"]:
                if position.xzDistanceTo(bot.kb["bed_position"]) < 2:
                    perceptions[PerceptionLabel.OWNBEDVISIBLE] = 1
                    break

        perceptions[PerceptionLabel.WOODINSIGHT] = 0
        if "Oak Log" in blocks_by_type:
            perceptions[PerceptionLabel.WOODINSIGHT] = 1
            bot.kb["wood_blocks"] = blocks_by_type["Oak Log"]

        # Update Practices Saliences
        for practice in practices:
            practice.update_salience(perceptions)
        practices.sort(reverse=True, key=lambda practice: practice.salience)

        # Update Ongoing Practice
        if ongoing_practice is not None:
            if not ongoing_practice.is_possible() or ongoing_practice.has_ended():
                print(f"Exit Practice {ongoing_practice}")
                ongoing_practice.exit()
                ongoing_practice = None
            else:
                print(f"Update Practice {ongoing_practice}")
                ongoing_practice.update()
        else:
            if practices[0].salience > 0:
                ongoing_practice = practices[0]
                print(f"Start Practice {ongoing_practice}")
                ongoing_practice.setup()
                if ongoing_practice.is_possible():
                    ongoing_practice.start()
            else:
                print("Do nothing")

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
