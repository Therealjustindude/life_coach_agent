from app.agent.life_coach_agent import LifeCoachAgent

def extract(agent, text):  # access the protected helper
    return agent._extract_action(text)

class DummyModel:
    def generate(self, prompt): return "ANSWER: ok"

def test_extract_action_name_only():
    a = LifeCoachAgent(DummyModel())
    assert extract(a, "THOUGHT: x\nACTION: now\nANSWER: y") == ("now", "")

def test_extract_action_with_arg():
    a = LifeCoachAgent(DummyModel())
    assert extract(a, "ACTION: draft_checklist: Update my resume\nANSWER: y") == ("draft_checklist", "Update my resume")

def test_no_action():
    a = LifeCoachAgent(DummyModel())
    assert extract(a, "THOUGHT: x\nANSWER: y") == (None, None)