"""
CLI to interact with Socialcraft
"""
import string
from sys import path
import cmd2
import toml
import pathlib
from socialcraft.agent_manager import AgentManager


class SocialCraftCli(cmd2.Cmd):
    """
    Socialcraft Cli
    """
    CMD_CATEGORY_AGENT_MANAGEMENT = "Agent Management"
    CMD_CATEGORY_BLUEPRINT_MANAGEMENT = "Blueprint Management"
    CMD_CATEGORY_UTILS = "Utility"

    def __init__(self):
        super().__init__()

        # CLEAN UP CLI
        self.remove_settable('debug')
        self.remove_settable('feedback_to_output')
        self.remove_settable('max_completion_items')
        self.remove_settable('quiet')
        self.remove_settable('timing')
        self.remove_settable('always_show_hint')
        self.remove_settable('echo')
        self.remove_settable('editor')
        self.remove_settable('allow_style')

        # HIDE DEFAULT COMMANDS
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_history
        del cmd2.Cmd.do_macro
        del cmd2.Cmd.do__relative_run_script
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_shortcuts
        del cmd2.Cmd.do_eof
        del cmd2.Cmd.do_run_script
        del cmd2.Cmd.do_shell

        self.prompt = '(SocialCraft) '

        # DEFINE SETTINGS
        self.minecraft_host = "host.docker.internal"
        self.minecraft_port = "25565"

        self.add_settable(
            cmd2.Settable('minecraft_host', string,
                          'host for the minecraft server', self))

        self.add_settable(
            cmd2.Settable('minecraft_port', int,
                          'port of the minecraft server', self))

        # STARTUP SOCIALCRAFT MANAGER
        self.manager = AgentManager(minecraft_host=self.minecraft_host,
                                    minecraft_port=self.minecraft_port)

    @cmd2.with_category(CMD_CATEGORY_AGENT_MANAGEMENT)
    def do_create(self):
        """
        Creates a new agent
        """
        self.poutput("Creating Agent")

    deploy_agent_argparser = cmd2.Cmd2ArgumentParser()
    deploy_agent_argparser.add_argument('name', type=str)

    @cmd2.with_argparser(deploy_agent_argparser)
    @cmd2.with_category(CMD_CATEGORY_AGENT_MANAGEMENT)
    def do_deploy(self, opts):
        """
        Deploys an agent
        """
        agent_name = opts.name
        self.poutput(f"Deploying Agent {agent_name}...")
        self.manager.deploy_agent(agent_name)
        self.poutput(f"Deployed agent {agent_name}!")

    @cmd2.with_category(CMD_CATEGORY_BLUEPRINT_MANAGEMENT)
    def do_generate(self, _):
        """
        Generates a new agent blueprint
        """
        self.poutput("Creating Blueprint")

    @cmd2.with_category(CMD_CATEGORY_UTILS)
    def do_load(self, file_path: str):
        """
        Loads a group of agents from a file specification
        """
        self.poutput(f"Processing file {file_path}...")
        toml_specification = toml.load(file_path)

        self.poutput("Loading blueprints...")

        toml_directory = pathlib.Path(pathlib.Path().resolve(),
                                      file_path).parents[0]

        blueprints_cache = {}
        blueprints = toml_specification['blueprints']

        self.poutput(f"{len(blueprints)} blueprints to generate...")
        for blueprint_key in blueprints:
            blueprint = blueprints[blueprint_key]
            directory_path = pathlib.Path(toml_directory,
                                          blueprint['directory'])
            self.poutput(
                f"Generating blueprint with name '{blueprint_key}' from {directory_path}..."
            )
            blueprints_cache[blueprint_key] = self.manager.generate_blueprint(
                blueprint_key, str(directory_path))
            self.poutput(f"Generated blueprint '{blueprint_key}'")

        agents = toml_specification['agents']

        self.poutput(f"{len(agents)} agents to generate...")
        for agent_key in agents:
            agent = agents[agent_key]

            self.poutput(
                f"Generating agent with name '{agent_key}' from blueprint {agent['blueprint']}..."
            )

            if agent['blueprint'] not in blueprints_cache:
                pass  # DO SOME ERROR HERE

            self.manager.create_agent(agent_key,
                                      blueprints_cache[agent['blueprint']])


def parse_file(file_path: str):
    """
    Parse File with agent specification
    """
    for agent in toml_content['agents']:
        print(toml_content['agents'][agent])