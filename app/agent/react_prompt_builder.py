from typing import Optional
from app.prompts.template import PROMPT_TEMPLATES

class ReactPromptBuilder:
    def __init__(self, coach_style: str, include_examples: bool = True):
        # Resolve template safely with default fallback
        self.template = PROMPT_TEMPLATES.get(coach_style, PROMPT_TEMPLATES["default"])
        self.include_examples = include_examples

    def build_prompt(self, context: Optional[str], user_input: str, tools_guide: Optional[str] = None) -> str:
        parts = [
            f"System: {self.template['system']}",
            f"Format:\n{self.template['format']}",
        ]
        
        if tools_guide:
            parts.append(f"Available Tools:\n{tools_guide}")
        
        if self.include_examples and self.template.get("examples"):
            example_str = "\n\n".join(
                f"Example Input: {ex['input']}\nExample Output:\n{ex['output']}"
                for ex in self.template["examples"]
            )
            parts.append(f"Examples:\n{example_str}")
        
        if context:
            ctx = context.strip()
            if ctx:
                parts.append(f"Context:\n{ctx}")
        
        parts.append(f"User: {user_input}")

        return "\n\n".join(parts).strip()