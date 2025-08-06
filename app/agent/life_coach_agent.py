import os
from app.memory.hybrid_memory import HybridMemory
from app.agent.prompt_builder import ReActPromptBuilder
from app.utils.logger import log_and_store_reasoning
from app.memory.reasoning_memory import ReasoningMemory

SHOW_THOUGHTS = os.getenv("SHOW_AGENT_THOUGHTS", "false").lower() == "true"

class LifeCoachAgent:
    def __init__(self, model):
        self.model = model
        self.memory = HybridMemory()
        self.reasoning_memory = ReasoningMemory()
        self.prompt_builder = ReActPromptBuilder()

    def chat(self, user_input, metadata=None):
        context = self.memory.get_context(user_input, where={"user_id": metadata.get("user_id")})
        prompt = self.prompt_builder.build(
            context=context,
            user_input=user_input,
            extra_instructions=["Respond as a supportive coach with actionable advice."]
        )

        response = self.model.generate(prompt)
        
        # Log reasoning to console
        log_to_console(metadata.get("user_id", "unknown"), response)

        # Save reasoning log in Chroma
        self.reasoning_memory.save(
            raw_response=response,
            user_id=metadata.get("user_id", "unknown"),
            session_id=metadata.get("session_id"),
            topic=metadata.get("topic")
        )

        # save the discussion
        self.memory.save(user_input, response, metadata=metadata)
        return self._extract_answer(response)
    
    def _extract_answer(self, response: str) -> str:
        """
        Extract only the ANSWER section unless debug mode is enabled.
        """
        if SHOW_THOUGHTS:
            return response
        # Try to find the 'ANSWER:' part
        parts = response.split("ANSWER:")
        return parts[-1].strip() if len(parts) > 1 else response