from javascript import require, On
import os
from csf_manager import Manager, CognitiveSocialFrame

minecraft_data = require("minecraft-data")
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


@On(bot, "spawn")
def handle(*args):
    print("I spawned 👋")

    mcData = require("minecraft-data")(bot.version)
    movements = pathfinder.Movements(bot, mcData)

    # Init  Cognitive Social Frames
    csf_manager = Manager()
    frame1 = CognitiveSocialFrame()
    frame1.add_affordances("CAN_JUMP")

    def issomeonearound(perceptions):
        if "other_player" in perceptions:
            return True

    frame1.add_salient_function(issomeonearound)
    csf_manager.add_frame(frame1)
    csf_manager.add_perception_to_buffer("other_player")
    csf_manager.update_saliences()

    print(csf_manager)
    print("Affordances: ")
    print(csf_manager.get_affordances())

    bot.setControlState("jump", True)


@On(bot, "end")
def handle(*args):
    print("Bot ended!", args)
