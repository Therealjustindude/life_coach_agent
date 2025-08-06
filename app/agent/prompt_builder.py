# app/agent/prompt_builder.py
from typing import List, Optional

class PromptBuilder:
    def __init__(
        self, 
        role: str = "You are an AI life coach. Be actionable, goal-oriented, and supportive."
    ):
        self.system_prompt = role

    def build(
        self,
        context: Optional[str],
        user_input: str,
        extra_instructions: Optional[List[str]] = None
    ) -> str:
        """
        Build a structured prompt combining system role, context, and user input.
        """
        # Prepare extra instructions if provided
        instructions_block = ""
        if extra_instructions:
            instructions_block = "\n".join(extra_instructions)

        # Prepare context block if provided
        context_block = ""
        if context:
            context_block = f"\nRelevant context:\n{context}\n"

        # Build the final structured prompt
        prompt = (
            f"{self.system_prompt}\n\n"
            f"{instructions_block}{context_block}\n"
            f"User request:\n{user_input}\n"
        )
        return prompt