# app/agent/tools/registry.py
from typing import Callable, Dict
from app.agent.tools.builtin import tool_now, tool_search_stub, tool_draft_checklist

class ToolRegistry:
    def __init__(self):
        # Map tool names to callables that accept a single string argument
        self._tools: Dict[str, Callable[[str], str]] = {
            "now": tool_now,
            "search": tool_search_stub,
            "draft_checklist": tool_draft_checklist,
        }

    def has(self, name: str) -> bool:
        return name in self._tools

    def run(self, name: str, arg: str) -> str:
        if not self.has(name):
            return f"Unknown tool: {name}"
        try:
            return self._tools[name](arg)
        except Exception as e:
            return f"Tool '{name}' error: {e}"