"""
Entrypoint for SocialCraft
"""
from socialcraft.cli.main import SocialCraftCli

import sys

cli = SocialCraftCli()
sys.exit(cli.cmdloop())
