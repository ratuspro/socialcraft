from socialcraft import AgentManager
import pathlib
import os
import random

if __name__ == "__main__":

    print("Starting Agent Manager...")
    manager = AgentManager(
        minecraft_host="10.68.166.113",
        minecraft_port=25565,
        minecraft_version="1.17",
    )
    print("Starting Agent Manager!")

    print("Creting Agent Blueprint...")
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)), "blueprint/")
    agent_blueprint = manager.generate_blueprint(name="builder", agent_source_path=str(path))
    print("Created Agent Blueprint!")

    print("Killing all dangling agents...")
    all_agents = manager.get_all_agents()
    for old_agent in all_agents:
        print(f"  Killing {old_agent.name}...")
        old_agent.kill()
        print(f"  RIP {old_agent.name}!")
    print("Killed all dangling agents!")

    input("Press Enter to deploy 20 agents...")

    for i in range(0, 20):
        agent_name = f"Agent_{i}"
        print(f"Deploying {agent_name}...")
        agent = manager.create_agent(
            agent_name,
            blueprint=agent_blueprint,
        )
        agent.deploy()
        print(f"Deployed {agent_name}!")

    print("Agents deployed!")
