import cmd2
import string

from socialcraft.agent_manager import AgentManager


class Socialcraft_cli(cmd2.Cmd):
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

        self.manager = AgentManager(minecraft_host=self.minecraft_host,
                                    minecraft_port=self.minecraft_port)
