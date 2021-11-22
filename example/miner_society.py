"""
Simple miner society
"""
import time
import pathlib
import random
from socialcraft import AgentManager
from socialcraft.agent import Agent, AgentStatus

if __name__ == "__main__":

    # Connect to Agent Manager
    manager = AgentManager(minecraft_host="host.docker.internal",
                           minecraft_port=25565)

    # Create Agent Blueprint
    path = pathlib.Path(pathlib.Path().resolve(), "example/images/simple_bot/")
    basic_miner = manager.create_blueprint(str(path))
    basic_miner.add_environment_variable("MINER_JUMPING_TIME", "2")

    # Create multiple agents with different settings
    agents = []

    for i in range(0, 10):
        agent = manager.create_agent(name="Agent" + str(i),
                                     blueprint=basic_miner)
        agents.append(agent)

    # Randomly deploy and withdraw agents every minute

    for _ in range(0, 50):
        agent: Agent = agents[random.randrange(0, 10)]

        if agent.status == AgentStatus.ONLINE:
            agent.withdraw()
        elif agent.status == AgentStatus.OFFLINE:
            agent.deploy()

        time.sleep(20)

    for i in range(0, 10):
        if agents[i].status == AgentStatus.PAUSED or agents[
                i].status == AgentStatus.ONLINE:
            agents[i].withdraw()
        agents[i].kill()
