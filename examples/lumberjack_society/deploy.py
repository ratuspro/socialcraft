import pathlib
import time
import random
from socialcraft import AgentManager, Agent, AgentStatus

if __name__ == "__main__":

    # Connect to Agent Manager
    manager = AgentManager(minecraft_host="host.docker.internal",
                           minecraft_port=25565)

    # Create Agent Blueprint
    path = pathlib.Path(pathlib.Path().resolve(),
                        "examples/lumberjack_society/blueprint/")
    lumberjack_blueprint = manager.generate_blueprint("lumberjack", str(path))

    # Create multiple agents with different settings
    agents = []

    for i in range(0, 3):
        agent = manager.create_agent(name="Agent" + str(i),
                                     blueprint=lumberjack_blueprint)
        agents.append(agent)

    # Randomly deploy and withdraw agents every minute

    for _ in range(0, 50):
        agent: Agent = agents[random.randrange(0, 3)]

        if agent.status == AgentStatus.ONLINE:
            agent.withdraw()
        elif agent.status == AgentStatus.OFFLINE:
            agent.deploy()

        time.sleep(10)

    for i in range(0, 3):
        if agents[i].status == AgentStatus.PAUSED or agents[
                i].status == AgentStatus.ONLINE:
            agents[i].withdraw()
        agents[i].kill()