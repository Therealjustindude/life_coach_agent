# app/agent/tools/builtin.py
from datetime import datetime, UTC

def tool_now(_: str = "") -> str:
    """Return current UTC timestamp."""
    return datetime.now(UTC).isoformat()

def tool_search_stub(query: str) -> str:
    """Fake search tool for development; replace later with real search."""
    q = (query or "").strip()
    if not q:
        return "No query provided."
    return f"[stubbed-search] Top notes about '{q}':\n- Note 1 ...\n- Note 2 ..."

def tool_draft_checklist(goal: str) -> str:
    """Draft a simple checklist from a goal string."""
    g = (goal or "").strip()
    if not g:
        return "No goal provided."
    return f"- Define the outcome for: {g}\n- Break into 3 steps\n- Schedule first step\n- Identify blockers\n- Review progress in 7 days"