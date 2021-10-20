import typer
import random
from agentDispatcher import create_agent, delete_agent, list_agents

app = typer.Typer()


@app.command()
def create(agent_name: str):
    create_agent(agent_name)


@app.command()
def list():
    list_agents()


@app.command()
def delete(agent_name: str):
    delete_agent(agent_name)


if __name__ == "__main__":
    app()
