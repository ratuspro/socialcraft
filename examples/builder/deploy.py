from socialcraft import AgentManager
import pathlib
import os
import random

if __name__ == "__main__":

    print("Starting Agent Manager...")
    manager = AgentManager(minecraft_host="10.68.166.113", minecraft_port=25565, minecraft_version="1.17")
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
    a1 = manager.create_agent(f"Agent1", blueprint=agent_blueprint, custom_envs={"bed": '{"x": 19, "y": 4, "z": 22}'})
    a1.deploy()

    a2 = manager.create_agent(f"Agent2", blueprint=agent_blueprint, custom_envs={"bed": '{"x": 19, "y": 4, "z": 26}'})
    a2.deploy()

    a3 = manager.create_agent(f"Agent3", blueprint=agent_blueprint, custom_envs={"bed": '{"x": 18, "y": 4, "z": 18}'})
    a3.deploy()

    a4 = manager.create_agent(f"Agent4", blueprint=agent_blueprint, custom_envs={"bed": '{"x": 15, "y": 4, "z": 21}'})
    a4.deploy()

    for i in range(0, 30):
        a = manager.create_agent("Agent_" + str(i), blueprint=agent_blueprint)
        a.deploy()

    print("Agents deployed!")
