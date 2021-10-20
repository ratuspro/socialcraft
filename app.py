import typer
from typer import main

from commands import agents

app = typer.Typer()

app.add_typer(agents.app, name="agents")

if __name__ == '__main__':
    app()
