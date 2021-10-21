import typer
from typer import main

from commands import agents

app = typer.Typer()

app.add_typer(agents.app, name="agent")

if __name__ == '__main__':
    app()
