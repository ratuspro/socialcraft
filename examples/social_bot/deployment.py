from socialcraft import AgentManager
import pathlib
import os

if __name__ == "__main__":

    # Connect to Agent Manager
    manager = AgentManager(minecraft_host="host.docker.internal",
                           minecraft_port=25565)

    # Create Agent Blueprint
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)),
                        "blueprint/")

    agent_blueprint = manager.generate_blueprint(name="friendly", agent_source_path=str(path))

    # Create Agent
    for i in range(0,10):
        name = f"friendly_joe_{str(i)}"
        old_agent = manager.get_agent(name)
 
        if old_agent is not None:
            old_agent.kill()

        new_joe = manager.create_agent(name=name, blueprint = agent_blueprint)
        new_joe.deploy()