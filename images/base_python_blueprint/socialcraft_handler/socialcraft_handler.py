import os
import string
from javascript import require, once
import logging
import sys
import pika
import time
from typing import Tuple, Optional

pathfinder = require("mineflayer-pathfinder")
mineflayer = require("mineflayer")


class Socialcraft_Handler:
    def __init__(self) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

        self.__config = {}
        self.__connection = None

        if "AGENT_NAME" in os.environ:
            self.__config["name"] = os.environ.get("AGENT_NAME") 
        else:
            raise Exception("No name received!")

        if "RABBITMQ_HOST" in os.environ:
            self.__config["brooker_host"] = os.environ.get("RABBITMQ_HOST") 
        else:
            raise Exception("No Brooker Host received!")

        if "RABBITMQ_PORT" in os.environ:
            self.__config["brooker_port"] = os.environ.get("RABBITMQ_PORT") 
        else:
            raise Exception("No Brooker port received!")

        if "RABBITMQ_VIRTUAL_HOST" in os.environ:
            self.__config["brooker_virtual_host"] = os.environ.get("RABBITMQ_VIRTUAL_HOST") 
        else:
            raise Exception("No Virtual Host received!")

        self.__logger.info("### Agent Setup Configuration:")
        self.__logger.info(f"Agent Name: {self.__config['name']}")
        self.__logger.info(f"Brooker Host: {self.__config['brooker_host']}")
        self.__logger.info(f"Brooker Port: {self.__config['brooker_port']}")
        self.__logger.info(f"Brooker Virtual Host: {self.__config['brooker_virtual_host']}")

    def connect(self):
        """
        Connects the agent to the message brooker, spawns it in minecraft and loads its dependencies
        """
        self.__logger.info("Connecting to Message Brooker...")
        while self.__connection is None:
            try:
                credentials = pika.PlainCredentials(self.name, self.name)
                self.__connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        self.__config["brooker_host"],
                        self.__config["brooker_port"],
                        self.__config["brooker_virtual_host"],
                        credentials,
                    )
                )
            except pika.exceptions.AMQPError as e:
                print(e)
                time.sleep(3)
                self.__logger.info("   Failed to connect. Trying again...")

        self.__logger.info("Declare Exchanges")
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(exchange="world", exchange_type="topic")
        self.__channel.exchange_declare(exchange="agent_state", exchange_type="direct")

        self.__logger.info("Setting up receiving queues")
        self.__world_queue_name = self.__channel.queue_declare(queue="").method.queue
        self.__agent_state_queue_name = self.__channel.queue_declare(queue=self.name).method.queue

        self.__channel.queue_bind(
            exchange="world",
            queue=self.__world_queue_name,
            routing_key=self.name,
        )

        self.__channel.queue_bind(
            exchange="agent_state",
            queue=self.__agent_state_queue_name,
            routing_key=self.name,
        )

        self.__logger.info("Connected to Message Brooker!")
        self.__logger.info("Fetching Variables from Brooker...")
        

        method_frame, header_frame, body = self.__channel.basic_get(queue=self.__agent_state_queue_name)
        while method_frame:
            elements = body.split(b":==")
            self.__config [elements[0].decode("utf-8") ] = elements[1].decode("utf-8") 
            self.__channel.basic_ack(method_frame.delivery_tag)
            method_frame, header_frame, body = self.__channel.basic_get(queue=self.__agent_state_queue_name)

        print(self.__config)

        botconfig = {
            "host": self.__config['MINECRAFT_HOST'],
            "port": self.__config['MINECRAFT_PORT'],
            "version": self.__config['MINECRAFT_VERSION'],
            "username": self.name,
            "password": self.__config['MINECRAFT_PASSWORD'],
        }

        self.__logger.info("Creating Bot...")
        self.__bot = mineflayer.createBot(botconfig)

        self.__logger.info("Loading plugins...")
        self.__bot.loadPlugin(pathfinder.pathfinder)

        self.__logger.info("Waiting for bot to spawn...")
        once(self.__bot, "spawn")
        self.__logger.info("Bot sucessfully spawned!")

        self.__logger.info("Setting up mineflayer-pathfinder...")
        self.mcData = require("minecraft-data")(self.__bot.version)
        movements = pathfinder.Movements(self.__bot, self.mcData)
        movements.allowSprinting = False
        movements.canDig = False
        self.__bot.pathfinder.setMovements(movements)

        self.__logger.info("Waiting for pathfinder...")
        while not self.__bot.hasPlugin(pathfinder.pathfinder):
            pass
        self.__logger.info("Pathfinder ready!")

    def send_message(
        self,
        position: Tuple[float, float, float],
        labels: list[str],
        message: str,
        target: str,
    ) -> None:
        """Sends a message using a message to the target agent

        Args:
            position (Tuple[float,float,float]): the position where the emitter sent the message from
            labels (list[str]): optional labels to describe the message
            message (str): the actual message
            target (str): the name of the target agent
        """
        self.__logger.debug(
            f"Sending from ({position[0]},{position[1]},{position[2]}) to {target} the following message: \n {message}"
        )

        self.__channel.basic_publish(
            "world",
            body=message,
            routing_key=target,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def receive_message(self) -> Optional[str]:
        """Attempts to receive a message addressed to this agent.
        If no message is available, return None

        Returns:
            str: message body
        """
        response = self.__channel.basic_get(self.__receiving_queue_name, auto_ack=True)
        if response[0] is not None:
            self.__logger.debug(f"Received the following message: {response[2]}")
        return response[2]

    @property
    def name(self) -> str:
        """Agent's name"""
        return self.__config["name"]

    @property
    def bot(self) -> mineflayer.Bot:
        """Returns mineflayer's bot associated with this agent"""
        if not self.__bot:
            self.__logger.error("Trying to get bot without establishing a connection first")
        return self.__bot

    def has_init_env_variable(self, name) -> bool:
        return name in self.__config

    def get_init_env_variable(self, name) -> str:
        return self.__config["name"]

    def __del__(self):
        self.__logger.info("Closing Brooker connection...")
        self.__connection.close()
        self.__logger.info("Brooker connection closed.")
