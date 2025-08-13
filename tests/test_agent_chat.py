from app.agent.life_coach_agent import LifeCoachAgent

class StubModelOnePass:
    def __init__(self): self.calls = 0
    def generate(self, prompt):
        self.calls += 1
        return "THOUGHT: none\nANSWER: Hello!"

class StubModelTwoPass:
    def __init__(self): self.calls = 0
    def generate(self, prompt):
        self.calls += 1
        if self.calls == 1:
            return "THOUGHT: need time\nACTION: now\nANSWER: (premature)"
        return "ANSWER: It’s 12:00 UTC."

def test_chat_no_tool_path(monkeypatch):
    agent = LifeCoachAgent(StubModelOnePass())
    out = agent.chat("hi", metadata={"user_id":"u1"})
    assert "Hello!" in out

def test_chat_with_tool_two_pass(monkeypatch):
    agent = LifeCoachAgent(StubModelTwoPass())
    out = agent.chat("what time is it?", metadata={"user_id":"u1"})
    assert "UTC" in out
    assert agent.model.calls == 2  # two calls when ACTION detected