from socialcraft import Agent


def test_agent_empty_creation():
    a = Agent(None, None)
    assert a is not None
