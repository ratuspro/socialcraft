from click.core import augment_usage_errors

agents = []


def create_agent(name: str):
    print(f"Creating agent with name {name}...")
    agents.append(name)
    print(f"Created agent {name}!")


def list_agents():
    print(f"All Agents:")
    for name in agents:
        print(">" + str(name))


def delete_agent(name: str):
    print(f"Deleting agent with name {name}...")
    agents.remove(name)
    print(f"Deleted agent {name}!")
