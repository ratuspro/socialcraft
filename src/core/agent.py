import docker


def connect_to_docker():
    client = docker.from_env()

    return client


def create_agent(name: str):
    print(f"Creating agent with name {name}...")
    client = connect_to_docker()
    print(
        client.containers.run('alpine',
                              'sleep 100',
                              name=f'agent_{name}',
                              labels=["socialcraft_agent"],
                              detach=True))
    print(f"Created agent {name}!")


def list_agents():
    print(f"All Agents:")
    client = connect_to_docker()
    containers = client.containers.list(
        filters={"label": ["socialcraft_agent"]})
    for container in containers:
        print(container.name)


def delete_agent(name: str):
    print(f"Deleting agent with name {name}...")
    client = connect_to_docker()

    client.containers.get(f'agent_{name}').remove()
