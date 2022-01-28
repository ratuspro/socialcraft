import pika
import time


class SocialcraftHandler:
    def __init__(self) -> None:
        self.__host = "host.docker.internal"
        self.__connection = None

    def load(self):
        while self.__connection is None:
            try:
                self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host="host.docker.internal"))
            except:
                time.sleep(3)
                print("Failed to connect. Trying again...")

        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue="hello")

    def __del__(self):
        print("gonna die")
        if self.__connection is not None:
            self.__connection.close()
