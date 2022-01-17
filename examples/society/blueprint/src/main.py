import random
from javascript import require, On, once
import os
from csf_manager import Manager, CognitiveSocialFrame, Perception, CSF_Utils
from utils import Utils

Vec3 = require("vec3").Vec3

pathfinder = require("mineflayer-pathfinder")
mineflayer = require("mineflayer")

botConfig = {
    "host": os.environ.get("MINECRAFT_HOST"),
    "port": os.environ.get("MINECRAFT_PORT"),
}

if "MINECRAFT_VERSION" in os.environ:
    botConfig["version"] = os.environ.get("MINECRAFT_VERSION")

if "MINECRAFT_USERNAME" in os.environ:
    botConfig["username"] = os.environ.get("MINECRAFT_USERNAME")
elif "AGENT_NAME" in os.environ:
    botConfig["username"] = os.environ.get("AGENT_NAME")

if "MINECRAFT_PASSWORD" in os.environ:
    botConfig["password"] = os.environ.get("MINECRAFT_PASSWORD")

if "MINECRAFT_VERSION" in os.environ:
    botConfig["version"] = os.environ.get("MINECRAFT_VERSION")

if "SOCIAL_GROUP" in os.environ:
    social_group = os.environ.get("SOCIAL_GROUP")


# Create bot
bot = mineflayer.createBot(botConfig)

# Load mineflayer-pathfinder
bot.loadPlugin(pathfinder.pathfinder)


# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Perceptions IDS
ID_PER_TIME_OF_DAY = "time_of_day"
ID_PER_DAY_OF_WEEK = "day_of_week"

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Affordances IDS
ID_AFF_LUMBERJACK = "lumberjack"
ID_AFF_WORSHIP = "worship"

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Knowledge Base
Workplace_Position = random.choice([Vec3(16, 4, -1), Vec3(21, 4, 7), Vec3(21, 4, -9)])
House_Position = random.choice([Vec3(50, 4, 30), Vec3(63, 4, 30), Vec3(75, 4, 30)])
Town_Plaza_Position = Vec3(86, 4, 17)
time_error = random.randint(-200, 200)
worship_day = random.choice(["THIRDDAY"])
pray_everyday = random.random() < 0.2

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Create Cognitive Social Frames
csf_manager = Manager()


# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Working Frame
work_frame = CognitiveSocialFrame()
work_frame.add_affordances(ID_AFF_LUMBERJACK)


def within_working_hours(perceptions):
    time_of_day = CSF_Utils.get_perception(perceptions, ID_PER_TIME_OF_DAY)
    week_day = CSF_Utils.get_perception(perceptions, ID_PER_DAY_OF_WEEK)
    return (
        time_of_day is not None
        and time_of_day.value > 2000 + time_error
        and time_of_day.value < 11000 + time_error
        and week_day is not None
        and week_day.value not in ["THIRDAY"]
    )


work_frame.add_salient_function(within_working_hours)
csf_manager.add_frame(work_frame)

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Praying Frame
worship_frame = CognitiveSocialFrame()
worship_frame.add_affordances(ID_AFF_WORSHIP)


def worship_time(perceptions):
    time_of_day = CSF_Utils.get_perception(perceptions, ID_PER_TIME_OF_DAY)
    week_day = CSF_Utils.get_perception(perceptions, ID_PER_DAY_OF_WEEK)
    return time_of_day is not None and (
        (pray_everyday and time_of_day.value > 100 and time_of_day.value < 1400)
        or (
            time_of_day.value > 300 + time_error
            and time_of_day.value < 4000 + time_error
            and week_day is not None
            and week_day.value == worship_day
        )
    )


worship_frame.add_salient_function(worship_time)
csf_manager.add_frame(worship_frame)


ready = False

once(bot, "spawn")
print("I spawned 👋")
mcdata = require("minecraft-data")(bot.version)
movements = pathfinder.Movements(bot, mcdata)
movements.canDig = False
movements.allowParkour = False
movements.allowSprinting = False
ready = True
bot.setControlState("sprint", False)
bot.pathfinder.setMovements(movements)


@On(bot, "time")
def handleTick(*args):

    # Add time of the day
    csf_manager.add_perception_to_buffer(
        Perception(ID_PER_TIME_OF_DAY, bot.time.timeOfDay)
    )

    # Add day of the week
    week_day = ""
    current_day = bot.time.bigTime // 24000

    if current_day % 3 == 0:
        week_day = "FIRSTADAY"
    elif current_day % 3 == 1:
        week_day = "SECONDAY"
    elif current_day % 3 == 2:
        week_day = "THIRDAY"
    csf_manager.add_perception_to_buffer(Perception(ID_PER_DAY_OF_WEEK, week_day))

    # New update
    csf_manager.update_saliences()

    # Execute plans
    execute_plans(bot)


def execute_plans(bot):

    if not ready:
        return
    affordances = csf_manager.get_affordances()
    Goal = None

    if ID_AFF_LUMBERJACK in affordances:

        if not bot.pathfinder.isMoving():
            if bot.entity.position.distanceTo(Workplace_Position) > 10:
                Goal = pathfinder.goals.GoalNear(
                    Workplace_Position.x,
                    Workplace_Position.y,
                    Workplace_Position.z,
                    1,
                )
            else:
                Goal = pathfinder.goals.GoalNear(
                    Workplace_Position.x + random.uniform(-1.5, 1.5),
                    Workplace_Position.y,
                    Workplace_Position.z + random.uniform(-1.5, 1.5),
                    1,
                )
    elif ID_AFF_WORSHIP in affordances:
        if not bot.pathfinder.isMoving():
            look_at = Town_Plaza_Position
            look_at.y += 1
            bot.lookAt(look_at)
            Goal = pathfinder.goals.GoalNear(
                Town_Plaza_Position.x + random.uniform(-3, 3),
                Town_Plaza_Position.y,
                Town_Plaza_Position.z + random.uniform(-3, 3),
                1,
            )
    else:
        if not bot.pathfinder.isMoving():
            if bot.entity.position.distanceTo(House_Position) > 10:
                Goal = pathfinder.goals.GoalNear(
                    House_Position["x"], House_Position["y"], House_Position["z"], 1
                )
            elif random.random() < 0.1:
                Goal = pathfinder.goals.GoalNear(
                    House_Position.x + random.uniform(-3, 3),
                    House_Position.y,
                    House_Position.z + random.uniform(-3, 3),
                    1,
                )

    if Goal is not None:
        bot.pathfinder.setGoal(Goal)
