from socialcraft import Agent


def test_agent_creation():
    agent = Agent(container=None, manager=None)
    assert agent is not None
