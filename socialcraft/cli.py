"""
SocialCraft Command Line Interface
"""
import typer
import commands

app = typer.Typer()

app.add_typer(commands.cli, name="agent")

if __name__ == '__main__':
    app()
