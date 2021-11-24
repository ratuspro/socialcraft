"""
Example Script: Start two agents
"""
from typing import List
import time
from socialcraft import AgentManager, Agent

if __name__ == "__main__":
    manager = AgentManager()

    agents: List[Agent] = []
    agents.append(manager.create_agent("Maria1"))
    agents.append(manager.create_agent("Maria2"))

    for agent in agents:
        agent.deploy()

    time.sleep(10)

    for agent in agents:
        agent.withdraw()

    for agent in agents:
        agent.kill()
