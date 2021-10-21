import docker
from docker import client


def connect_to_docker():
    client = docker.from_env()
    return client


def get_container(name: str, client: docker.DockerClient):
    container = client.containers.get(name)
    return container


def create_agent(name: str):
    client = connect_to_docker()
    client.containers.create('ubuntu',
                             'sleep 300',
                             name=name,
                             labels=["socialcraft_agent"],
                             detach=True)


def get_all_agents():
    client = connect_to_docker()
    containers = client.containers.list(
        filters={'label': ["socialcraft_agent"]})
    return containers


def deploy_agent(name: str):
    client = connect_to_docker()
    try:
        container = get_container(name, client)
        container.start()

    except docker.errors.NotFound:
        print("Agent not found")


def pause_agent(name: str):
    client = connect_to_docker()
    try:
        container = get_container(name, client)
        container.pause()

    except docker.errors.NotFound:
        print("Agent not found")


def resume_agent(name: str):
    client = connect_to_docker()
    try:
        container = get_container(name, client)
        container.unpause()

    except docker.errors.NotFound:
        print("Agent not found")


def kill_agent(name: str):
    client = connect_to_docker()
    try:
        container = get_container(name, client)
        container.stop()

    except docker.errors.NotFound:
        print("Agent not found")


def delete_agent(name: str):
    client = connect_to_docker()
    try:
        container = get_container(name, client)
        container.remove(force=True)

    except docker.errors.NotFound:
        print("Agent not found")
