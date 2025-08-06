# app/agent/react_prompt_builder.py
from typing import Optional, List

class ReActPromptBuilder:
    def __init__(self, role: str = "You are an AI life coach. Think step-by-step to give actionable, structured advice."):
        self.system_prompt = role

    def build(
        self,
        context: Optional[str],
        user_input: str,
        extra_instructions: Optional[List[str]] = None
    ) -> str:
        """
        Build a ReAct-style prompt with instructions for reasoning.
        """
        instructions_block = "\n".join(extra_instructions) if extra_instructions else ""
        context_block = f"\nRelevant context:\n{context}\n" if context else ""

        return f"""{self.system_prompt}

{instructions_block}{context_block}

Follow this reasoning format:
THOUGHT: Explain your internal reasoning to plan the response.
ACTION: (Optional) Indicate if you'd take an action (e.g., query memory or external tools).
ANSWER: Provide a clear, step-by-step actionable answer for the user.

User request:
{user_input}
"""