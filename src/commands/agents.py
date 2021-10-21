from docker.types import containers
import typer
from tabulate import tabulate
from core import create_agent, delete_agent, get_all_agents, deploy_agent, kill_agent, pause_agent, resume_agent

app = typer.Typer()


@app.command()
def create(agent_name: str):
    """
    Create a new agent with agent_name
    """
    create_agent(agent_name)


@app.command()
def list():
    """
    List all the agents 
    """
    containers = get_all_agents()
    table = [[
        container.name, container.status, container.labels,
        container.attrs['Config']['Env']
    ] for container in containers]

    typer.echo(
        tabulate(table,
                 headers=["Name", "Status", "Labels", "Env"],
                 tablefmt="fancy_grid"))


@app.command()
def deploy(agent_name: str):
    """
    Deploys the agent
    """
    deploy_agent(agent_name)


@app.command()
def pause(agent_name: str):
    """
    Pauses the agent
    """
    pause_agent(agent_name)


@app.command()
def resume(agent_name: str):
    """
    Resumes the agent
    """
    resume_agent(agent_name)


@app.command()
def kill(agent_name: str):
    """
    Kill the agent
    """
    kill_agent(agent_name)


@app.command()
def delete(agent_name: str):
    """
    Deletes the agent and all related data
    """
    delete_agent(agent_name)


if __name__ == "__main__":
    app()
