"""
SocialCraft Command Line Interface
"""
import typer
from socialcraft import commands

app = typer.Typer()

app.add_typer(commands.cli, name="agent")
