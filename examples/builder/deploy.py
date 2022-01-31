from socialcraft import AgentManager
import pathlib
import os
import random

if __name__ == "__main__":

    print("Starting Agent Manager...")
    manager = AgentManager(minecraft_host="10.68.166.113", minecraft_port=25565)
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

    print("Deploying Agents...")
    a1 = manager.create_agent(f"Agent1", blueprint=agent_blueprint)
    a1.deploy()

    a2 = manager.create_agent(f"Agent2", blueprint=agent_blueprint)
    a2.deploy()

    a3 = manager.create_agent(f"Agent3", blueprint=agent_blueprint)
    a3.deploy()

    a4 = manager.create_agent(f"Agent4", blueprint=agent_blueprint)
    a4.deploy()

    print("Agents deployed!")
