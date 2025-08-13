from app.agent.tools.registry import ToolRegistry

def test_describe_lists_tools():
    reg = ToolRegistry()
    guide = reg.describe()
    assert "now" in guide and "draft_checklist" in guide

def test_run_known_tool():
    reg = ToolRegistry()
    out = reg.run("now", "")
    assert isinstance(out, str) and len(out) > 10  # iso-ish

def test_unknown_tool_message():
    reg = ToolRegistry()
    out = reg.run("not_a_tool", "")
    assert "Unknown tool" in out or "unavailable" in out.lower()