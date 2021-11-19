"""
Entrypoint for SocialCraft
"""
from socialcraft.cli.main import Socialcraft_cli

import sys

cli = Socialcraft_cli()
sys.exit(cli.cmdloop())
