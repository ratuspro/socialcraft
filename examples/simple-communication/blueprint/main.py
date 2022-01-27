from socialcraft_handler import Socialcraft_Handler
import time

handler = Socialcraft_Handler()
handler.connect()

time.sleep(2)

print(handler.receive_message())

time.sleep(2)

handler.send_message(
    position=(0, 5, 0),
    labels=[],
    message=f"Hello from {handler.name}!",
    target=("Interlocutor1" if handler.name == "Interlocutor2" else "Interlocutor2"),
)

time.sleep(2)

print(handler.receive_message())

time.sleep(2)

handler.send_message(
    position=(0, 0, 0),
    labels=[],
    message=f"Hello from {handler.name}!",
    target=("Interlocutor1" if handler.name == "Interlocutor2" else "Interlocutor2"),
)

time.sleep(2)

print(handler.receive_message())
