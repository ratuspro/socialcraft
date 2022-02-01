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
    beds = [
        '{"x": 30, "y": 4, "z": 30}',
        '{"x": 30, "y": 4, "z": 33}',
        '{"x": 29, "y": 4, "z": 38}',
        '{"x": 31, "y": 4, "z": 41}',
        '{"x": 31, "y": 4, "z": 38}',
    ]

    workplaces = [
        '{"x": 12, "y": 3, "z": 38}',
        '{"x": 12, "y": 3, "z": 46}',
        '{"x": 12, "y": 3, "z": 38}',
        '{"x": 19, "y": 3, "z": 51}',
        '{"x": 29, "y": 3, "z": 52}',
    ]

    agent1 = manager.create_agent(
        f"Agent1",
        blueprint=agent_blueprint,
        custom_envs={"rel": '{"friends": ["Agent2"]}', "bed": beds[0], "workplace": workplaces[0]},
    )
    agent1.deploy()

    agent2 = manager.create_agent(
        f"Agent2",
        blueprint=agent_blueprint,
        custom_envs={"rel": '{"friends": ["Agent1", "Agent4", "Agent5"]}', "bed": beds[1], "workplace": workplaces[1]},
    )
    agent2.deploy()

    agent3 = manager.create_agent(
        f"Agent3",
        blueprint=agent_blueprint,
        custom_envs={"rel": '{"friends": ["Agent4", "Agent5"]}', "bed": beds[2], "workplace": workplaces[2]},
    )
    agent3.deploy()

    agent4 = manager.create_agent(
        f"Agent4",
        blueprint=agent_blueprint,
        custom_envs={"rel": '{"friends": ["Agent3", "Agent5"]}', "bed": beds[3], "workplace": workplaces[3]},
    )
    agent4.deploy()

    agent5 = manager.create_agent(
        f"Agent5",
        blueprint=agent_blueprint,
        custom_envs={"rel": '{"friends": ["Agent3", "Agent4"]}', "bed": beds[4], "workplace": workplaces[4]},
    )
    agent5.deploy()

    print("Agents deployed!")
