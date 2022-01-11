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
    joe = manager.create_agent(name="friendly_joe", blueprint = agent_blueprint)

    joe.deploy()


