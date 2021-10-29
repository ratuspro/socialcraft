"""
Agents Command
"""
import typer
from tabulate import tabulate
from socialcraft import AgentManager

cli = typer.Typer()

manager = AgentManager(docker_url="npipe:////./pipe/docker_engine")


@cli.command()
def create(agent_name: str):
    """
    Create a new agent with agent_name
    """
    manager.create_agent(agent_name)


@cli.command("list")
def cli_list():
    """
    List all the agents
    """
    agents = manager.get_all_agents()
    table = [[agent.name, agent.status] for agent in agents]

    typer.echo(
        tabulate(table, headers=["Name", "Status"], tablefmt="fancy_grid"))


@cli.command()
def deploy(agent_name: str):
    """
    Deploys the agent
    """
    manager.deploy_agent(agent_name)


@cli.command()
def pause(agent_name: str):
    """
    Pauses the agent
    """
    manager.pause_agent(agent_name)


@cli.command()
def resume(agent_name: str):
    """
    Resumes the agent
    """
    manager.resume_agent(agent_name)


@cli.command()
def withdraw(agent_name: str):
    """
    Withdraw the agent
    """
    manager.withdraw_agent(agent_name)


@cli.command()
def kill(agent_name: str):
    """
    Kills the agent and all related data
    """
    manager.kill_agent(agent_name)


if __name__ == "__main__":
    cli()
