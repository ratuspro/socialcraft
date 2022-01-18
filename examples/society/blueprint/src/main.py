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

is_father = False
if "father" in os.environ:
    is_father = os.environ.get("father")

print(is_father)

# Create bot
bot = mineflayer.createBot(botConfig)

# Load mineflayer-pathfinder
bot.loadPlugin(pathfinder.pathfinder)


# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Perceptions IDS
ID_PER_TIME_OF_DAY = "time_of_day"
ID_PER_DAY_OF_WEEK = "day_of_week"
ID_PER_RESPECTABLE_FIGURE = "respectable"

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Affordances IDS
ID_AFF_LUMBERJACK = "lumberjack"
ID_AFF_WORSHIP = "worship"
ID_AFF_SUBSERVIENT = "subservient"
ID_AFF_SURVEIL = "surveil"
ID_AFF_VISIT_HOUSE = "visit_citizens"

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Knowledge Base
Workplace_Position = random.choice([Vec3(16, 4, -1), Vec3(21, 4, 7), Vec3(21, 4, -9)])
House_Position = random.choice([Vec3(50, 4, 30), Vec3(63, 4, 30), Vec3(75, 4, 30)])

if is_father:
    House_Position = Vec3(74, 4, 11)
Town_Plaza_Position = Vec3(86, 4, 17)
time_error = random.randint(-200, 200)
worship_day = random.choice(["THIRDAY"])
pray_everyday = random.random() < 0.2
# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Create Cognitive Social Frames
csf_manager = Manager()


# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Working Frame
work_frame = CognitiveSocialFrame()
work_frame.add_affordances(ID_AFF_LUMBERJACK)


def within_working_hours(perceptions, bot):
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
if not is_father:
    csf_manager.add_frame(work_frame)

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Praying Frame
worship_frame = CognitiveSocialFrame()
worship_frame.add_affordances(ID_AFF_WORSHIP)


def worship_time(perceptions, bot):
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
if not is_father:
    csf_manager.add_frame(worship_frame)

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Respect Frame
respect_frame = CognitiveSocialFrame()
respect_frame.add_affordances(ID_AFF_SUBSERVIENT)


def respectable_nearby(perceptions, bot):
    for entity_key in bot.entities:
        if (
            bot.entities[entity_key].name == "player"
            and "Father" in bot.entities[entity_key].username
        ):
            distance = pow(
                bot.entity.position.x - bot.entities[entity_key].position.x, 2
            ) + pow(bot.entity.position.z - bot.entities[entity_key].position.z, 2)
            if distance < 25:
                return True
    return False


respect_frame.add_salient_function(respectable_nearby)
if not is_father:
    csf_manager.add_frame(respect_frame)

# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# SurveilWork Frame
surveil = CognitiveSocialFrame()
surveil.add_affordances(ID_AFF_SURVEIL)


def should_surveil(perceptions, bot):
    time_of_day = CSF_Utils.get_perception(perceptions, ID_PER_TIME_OF_DAY)
    week_day = CSF_Utils.get_perception(perceptions, ID_PER_DAY_OF_WEEK)
    return (
        time_of_day is not None
        and time_of_day.value > 600 + time_error
        and time_of_day.value < 4500 + time_error
        and week_day is not None
        and week_day.value != worship_day
    )


surveil.add_salient_function(should_surveil)
if is_father:
    csf_manager.add_frame(surveil)


# =#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
# Visit Citizens Frame
visit_citizens = CognitiveSocialFrame()
visit_citizens.add_affordances(ID_AFF_VISIT_HOUSE)


def should_pay_visit(perceptions, bot):
    time_of_day = CSF_Utils.get_perception(perceptions, ID_PER_TIME_OF_DAY)
    week_day = CSF_Utils.get_perception(perceptions, ID_PER_DAY_OF_WEEK)
    return (
        time_of_day is not None
        and time_of_day.value > 400 + time_error
        and time_of_day.value < 4000 + time_error
        and week_day is not None
        and week_day.value == worship_day
    )


visit_citizens.add_salient_function(should_pay_visit)
if is_father:
    csf_manager.add_frame(visit_citizens)

ready = False
once(bot, "spawn")
print("I spawned 👋")
mcdata = require("minecraft-data")(bot.version)
movements = pathfinder.Movements(bot, mcdata)
movements.canDig = False
movements.allowParkour = False
movements.allowSprinting = False
bot.setControlState("sprint", False)
bot.pathfinder.setMovements(movements)
ready = True


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
    csf_manager.update_saliences(bot)

    # Execute plans
    execute_plans(bot)


def execute_plans(bot):

    if not ready:
        return
    time_since_last_update = 0
    print("New Tick:")
    affordances = csf_manager.get_affordances()
    print(affordances)
    Goal = None

    if ID_AFF_VISIT_HOUSE in affordances:

        next_house = random.choice([Vec3(50, 4, 30), Vec3(63, 4, 30), Vec3(75, 4, 30)])

        if not bot.pathfinder.isMoving():
            Utils.chat_if_close(
                "Let's say hi to another citizen!", bot.entity.position, bot
            )
            if bot.entity.position.distanceTo(next_house) > 5:
                Goal = pathfinder.goals.GoalNear(
                    next_house.x,
                    next_house.y,
                    next_house.z,
                    1,
                )
            else:
                Goal = pathfinder.goals.GoalNear(
                    next_house.x + random.uniform(-3, 3),
                    next_house.y,
                    next_house.z + random.uniform(-3, 3),
                    1,
                )
    elif ID_AFF_SURVEIL in affordances:

        next_workplace = random.choice(
            [Vec3(16, 4, -1), Vec3(21, 4, 7), Vec3(21, 4, -9)]
        )

        if not bot.pathfinder.isMoving():
            if bot.entity.position.distanceTo(next_workplace) > 5:
                Utils.chat_if_close(
                    "Time to see what my citizens are doing.", bot.entity.position, bot
                )
                Goal = pathfinder.goals.GoalNear(
                    next_workplace.x,
                    next_workplace.y,
                    next_workplace.z,
                    1,
                )
            else:
                Utils.chat_if_close(
                    "Seems like they are working.", bot.entity.position, bot
                )
                Goal = pathfinder.goals.GoalNear(
                    next_workplace.x + random.uniform(-1.5, 1.5),
                    next_workplace.y,
                    next_workplace.z + random.uniform(-1.5, 1.5),
                    1,
                )

    elif ID_AFF_SUBSERVIENT in affordances:
        bot.pathfinder.stop()
        for entity_key in bot.entities:
            entity = bot.entities[entity_key]
            if entity.name == "player" and "Father" in entity.username:
                Utils.chat_if_close(
                    f"It's {entity.username}!", bot.entity.position, bot
                )
                bot.lookAt(entity.position)
                break

    elif ID_AFF_LUMBERJACK in affordances:

        if not bot.pathfinder.isMoving():
            if bot.entity.position.distanceTo(Workplace_Position) > 10:
                Utils.chat_if_close("Another day of work", bot.entity.position, bot)
                Goal = pathfinder.goals.GoalNear(
                    Workplace_Position.x,
                    Workplace_Position.y,
                    Workplace_Position.z,
                    1,
                )
            else:
                Utils.chat_if_close("Working a bit more...", bot.entity.position, bot)
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
            Utils.chat_if_close(
                "Feels good to visit the plaza", bot.entity.position, bot
            )
    else:
        if not bot.pathfinder.isMoving():
            if bot.entity.position.distanceTo(House_Position) > 10:
                Utils.chat_if_close("Time to go home", bot.entity.position, bot)
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
