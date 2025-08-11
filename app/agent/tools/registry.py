# app/agent/tools/registry.py
from typing import Callable, Dict, Tuple
from app.agent.tools.builtin import tool_now, tool_search_stub, tool_draft_checklist

class ToolRegistry:
    def __init__(self):
        # name -> (callable, description)
        self._tools: Dict[str, Tuple[Callable[[str], str], str]] = {
            "now": (tool_now, "Returns the current UTC date and time."),
            "search": (tool_search_stub, "Searches for information about a query. (stub in dev)"),
            "draft_checklist": (tool_draft_checklist, "Generates a short actionable checklist for a goal."),
        }

    def has(self, name: str) -> bool:
        return name in self._tools

    def run(self, name: str, arg: str) -> str:
        if not self.has(name):
            return f"Unknown tool: {name}"
        fn, _ = self._tools[name]
        try:
            return fn(arg)
        except Exception as e:
            return f"Tool '{name}' error: {e}"

    def describe(self) -> str:
        lines = []
        for name, (_, desc) in self._tools.items():
            if name == "search":
                lines.append(f"- {name}: <query> → {desc}")
            elif name == "draft_checklist":
                lines.append(f"- {name}: <goal> → {desc}")
            else:
                lines.append(f"- {name} → {desc}")
        return "\n".join(lines)