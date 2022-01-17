from socialcraft import AgentManager
import pathlib
import os
import random

if __name__ == "__main__":

    # Connect to Agent Manager
    manager = AgentManager(minecraft_host="host.docker.internal", minecraft_port=25565)

    # Create Agent Blueprint
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)), "blueprint/")

    agent_blueprint = manager.generate_blueprint(
        name="social_bot", agent_source_path=str(path)
    )

    all_agents = manager.get_all_agents()

    for old_agent in all_agents:
        old_agent.withdraw()

    for old_agent in all_agents:
        old_agent.kill()

    for i in range(0, 9):
        agent = manager.create_agent(f"Joe{i}", blueprint=agent_blueprint)
        agent.deploy()
