import typer
from core import create_agent, delete_agent, get_all_agents

app = typer.Typer()


@app.command()
def create(agent_name: str):
    create_agent(agent_name)


@app.command()
def list():
    for container in get_all_agents():
        typer.echo(container)


@app.command()
def delete(agent_name: str):
    delete_agent(agent_name)


if __name__ == "__main__":
    app()
