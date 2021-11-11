"""
Simple miner society
"""
import time
import pathlib
from socialcraft import AgentManager

if __name__ == "__main__":

    # Connect to Agent Manager
    manager = AgentManager(minecraft_host="host.docker.internal",
                           minecraft_port=25565)

    # Create Agent Blueprint
    path = pathlib.Path(pathlib.Path().resolve(), "example/images/simple_bot/")
    basic_miner = manager.create_blueprint(str(path))

    # Create multiple agents with different settings
    agents = []
    for i in range(0, 10):
        agent = manager.create_agent(name="Agent" + str(i), blueprint)

    agents.append(manager.create_agent)

    # Randomly deploy and withdraw agents every minute

    while True:
        agent = manager.create_agent(name="MaAgent", blueprint=basic_miner)
        time.sleep(10)
        agent.deploy()
        time.sleep(10)
        agent.pause()
        time.sleep(10)
        agent.withdraw()
        time.sleep(10)
        agent.kill()
        time.sleep(10)
