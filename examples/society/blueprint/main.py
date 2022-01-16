from javascript import require, On, Once, AsyncTask, once, off
import os

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

bot = mineflayer.createBot(botConfig)


@On(bot, "chat")
def onChat(this, user, message, *rest):
    print(f'{user} said "{message}"')

    # If the message contains stop, remove the event listener and stop logging.
    if "stop" in message:
        off(bot, "chat", onChat)


# The spawn event
once(bot, "login")
bot.chat("I spawned")
print("Hello, I'm alive")
