from app.memory.hybrid_memory import HybridMemory
from app.agent.react_prompt_builder import ReactPromptBuilder
from app.utils.logger import log_to_console
from app.memory.reasoning_memory import ReasoningMemory
from app.memory.conversation_buffer_memory import ConversationBufferMemory
from app.memory.chroma_memory import ChromaMemory
from app.utils.get_env import get_env


SHOW_THOUGHTS = get_env("SHOW_AGENT_THOUGHTS", "false").lower() == "true"

class LifeCoachAgent:
    def __init__(
        self, 
        model, 
        coach_style: str | None = None, 
        include_examples: bool | None = None
    ):
        self.model = model
        self.memory = HybridMemory(buffer=ConversationBufferMemory(), vector_store=ChromaMemory())
        self.reasoning_memory = ReasoningMemory()
        self.prompt_builder = ReactPromptBuilder(coach_style=coach_style, include_examples=include_examples)

    def chat(self, user_input, metadata=None):
        filters = {}
        if metadata:
            if uid := metadata.get("user_id"):
                filters["user_id"] = uid
            if sid := metadata.get("session_id"):
                filters["session_id"] = sid

        context = self.memory.get_context(
            user_input,
            where=filters or None,
            limit=8,
            top_k=5,
            summarize_threshold=1400,
            summarize_fn=self._summarize_with_model
        )

        prompt = self.prompt_builder.build_prompt(
            context=context,
            user_input=user_input
        )

        try:
            response = self.model.generate(prompt)
        except Exception as e:
            # log & friendly fallback
            log_to_console(metadata.get("user_id", "unknown"), f"[MODEL_ERROR] {e}")
            response = (
                "ANSWER: I hit a hiccup generating a full response just now. "
                "Here's a quick next step: write down your top objective for this week, "
                "and the single smallest action you can take today to move toward it."
            )
        
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
    

    def _summarize_with_model(self, prompt: str) -> str:
        return self.model.generate(prompt)

    def _extract_answer(self, response: str) -> str:
        """
        Extract only the ANSWER section unless debug mode is enabled.
        """
        if SHOW_THOUGHTS:
            return response
        # Try to find the 'ANSWER:' part
        parts = response.split("ANSWER:")
        return parts[-1].strip() if len(parts) > 1 else response