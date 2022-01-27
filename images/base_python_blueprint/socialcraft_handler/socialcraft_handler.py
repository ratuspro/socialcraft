import os
from javascript import require, once
import logging
import sys
import pika
import time

pathfinder = require("mineflayer-pathfinder")
mineflayer = require("mineflayer")


class Socialcraft_Handler:
    def __init__(self) -> None:

        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

        self.__botConfig = {}
        self.__connection = None

        if "MINECRAFT_USERNAME" in os.environ:
            self.__botConfig["username"] = os.environ.get("MINECRAFT_USERNAME")
        elif "AGENT_NAME" in os.environ:
            self.__botConfig["username"] = os.environ.get("AGENT_NAME")

        self.__botConfig["host"] = (
            os.environ.get("MINECRAFT_HOST")
            if "MINECRAFT_HOST" in os.environ
            else "localhost"
        )

        self.__botConfig["port"] = (
            os.environ.get("MINECRAFT_PORT")
            if "MINECRAFT_PORT" in os.environ
            else "25565"
        )

        self.__botConfig["password"] = (
            os.environ.get("MINECRAFT_PASSWORD")
            if "MINECRAFT_PASSWORD" in os.environ
            else ""
        )

        self.__botConfig["version"] = (
            os.environ.get("MINECRAFT_VERSION")
            if "MINECRAFT_VERSION" in os.environ
            else False
        )

        self.__botConfig["brooker_host"] = (
            os.environ.get("RABBITMQ_HOST")
            if "RABBITMQ_HOST" in os.environ
            else "localhost"
        )

        self.__botConfig["brooker_port"] = (
            os.environ.get("RABBITMQ_PORT") if "RABBITMQ_PORT" in os.environ else 5672
        )

        self.__botConfig["brooker_virtual_host"] = (
            os.environ.get("RABBITMQ_VIRTUAL_HOST")
            if "RABBITMQ_VIRTUAL_HOST" in os.environ
            else "/"
        )

        self.__logger.info("### Agent Setup Configuration:")
        self.__logger.info(f"Minecraft Host: {self.__botConfig['host']}")
        self.__logger.info(f"Minecraft Port: {self.__botConfig['port']}")
        self.__logger.info(f"Minecraft Version: {self.__botConfig['version']}")
        self.__logger.info(f"Minecraft Username: {self.__botConfig['username']}")
        self.__logger.info(f"Minecraft Password: {self.__botConfig['username']}")
        self.__logger.info(f"Agent Name: {self.__botConfig['username']}")
        self.__logger.info(f"Brooker Host: {self.__botConfig['brooker_host']}")
        self.__logger.info(f"Brooker Port: {self.__botConfig['brooker_port']}")
        self.__logger.info(
            f"Brooker Virtual Host: {self.__botConfig['brooker_virtual_host']}"
        )

    def connect(self):
        self.__logger.info("1. Connecting to Message Brooker...")
        while self.__connection is None:
            try:
                credentials = pika.PlainCredentials(self.name, self.name)
                self.__connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        self.__botConfig["brooker_host"],
                        self.__botConfig["brooker_port"],
                        self.__botConfig["brooker_virtual_host"],
                        credentials,
                    )
                )
            except pika.exceptions.AMQPError as e:
                print(e)
                time.sleep(3)
                self.__logger.info("1. Failed to connect. Trying again...")

        self.__channel = self.__connection.channel()
        self.__logger.info("1. Connected to Message Brooker!")

        self.__logger.info("2. Creating Bot...")
        self.__bot = mineflayer.createBot(self.__botConfig)

        self.__logger.info("3. Loading plugins...")
        self.__bot.loadPlugin(pathfinder.pathfinder)

        self.__logger.info("2. Waiting for bot to spawn...")
        once(self.__bot, "spawn")
        self.__logger.info("2. Bot sucessfully spawned!")

        self.__logger.info("3. Setting up mineflayer-pathfinder...")
        mcData = require("minecraft-data")(self.__bot.version)
        movements = pathfinder.Movements(self.__bot, mcData)
        self.__bot.pathfinder.setMovements(movements)

        self.__logger.info("3. Waiting for pathfinder...")
        while not self.__bot.hasPlugin(pathfinder.pathfinder):
            pass
        self.__logger.info("3. Pathfinder ready!")

    @property
    def name(self):
        return self.__botConfig["username"]

    @property
    def bot(self):
        if not self.__bot:
            self.__logger.error(
                "Trying to get bot without establishing a connection first"
            )
        return self.__bot
