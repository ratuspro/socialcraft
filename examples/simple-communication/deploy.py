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
    interlocutor_blueprint = manager.generate_blueprint(name="interlocutor", agent_source_path=str(path))
    print("Created Agent Blueprint!")

    print("Killing all dangling agents...")
    all_agents = manager.get_all_agents()
    for old_agent in all_agents:
        print(f"  Killing {old_agent.name}...")
        old_agent.kill()
        print(f"  RIP {old_agent.name}!")
    print("Killed all dangling agents!")

    print("Deploying Interlocutor 1...")
    int1 = manager.create_agent(f"Interlocutor1", blueprint=interlocutor_blueprint)
    int1.deploy()
    print("Interlocutor 1 deployed!")

    print("Interlocutor 2 Agent...")
    int2 = manager.create_agent(f"Interlocutor2", blueprint=interlocutor_blueprint)
    int2.deploy()
    print("Interlocutor 2 deployed!")
