from app.memory.hybrid_memory import HybridMemory
from app.agent.react_prompt_builder import ReactPromptBuilder
from app.utils.logger import log_to_console
from app.memory.reasoning_memory import ReasoningMemory
from app.memory.conversation_buffer_memory import ConversationBufferMemory
from app.memory.chroma_memory import ChromaMemory
from app.utils.get_env import get_env
from app.agent.tools.registry import ToolRegistry

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
        self.tools = ToolRegistry()
        self.tools_guide = self.tools.describe()

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
            tools_guide=self.tools_guide
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
        
        # Log reasoning to console for first pass
        log_to_console(metadata.get("user_id", "unknown"), response)

        # Save first-pass reasoning trace
        self.reasoning_memory.save(
            raw_response=response,
            user_id=metadata.get("user_id", "unknown"),
            session_id=metadata.get("session_id"),
            topic=metadata.get("topic")
        )

        # Try to parse and execute an ACTION
        tool_name, tool_arg = self._extract_action(response)
        if tool_name and self.tools and self.tools.has(tool_name):
            tool_result = self.tools.run(tool_name, tool_arg or "")

            # Build a follow-up prompt that includes tool output, then get final answer
            post_tool_instruction = (
                "Post-Tool Instruction:\n"
                "Now that TOOL RESULT is available, do not include THOUGHT or ACTION in your next message.\n"
                "Provide only the final ANSWER."
            )
            enriched_context = (
                f"{context}\n\nTOOL RESULT ({tool_name}):\n{tool_result}\n\n{post_tool_instruction}"
            )
            followup_prompt = self.prompt_builder.build_prompt(
                context=enriched_context,
                user_input=user_input,
                tools_guide=self.tools_guide
            )
            try:
                second = self.model.generate(followup_prompt)
            except Exception as e:
                log_to_console(metadata.get("user_id", "unknown"), f"[MODEL_ERROR] {e}")
                second = (
                    "ANSWER: I ran into an issue finalizing the answer after using a tool. "
                    "Quick next step: write down your top objective for this week and the smallest action to take today."
                )

            # Log and store second-pass reasoning
            log_to_console(metadata.get("user_id", "unknown"), second)
            self.reasoning_memory.save(
                raw_response=second,
                user_id=metadata.get("user_id", "unknown"),
                session_id=metadata.get("session_id"),
                topic=metadata.get("topic")
            )

            # Save final exchange to chat memory and return final answer
            self.memory.save(user_input, second, metadata=metadata)
            return self._extract_answer(second)

        # No tool path → save first pass and return
        self.memory.save(user_input, response, metadata=metadata)
        return self._extract_answer(response)
    

    def _extract_action(self, response: str) -> tuple[str | None, str | None]:
        """Extract (tool_name, arg) from an ACTION block in the model response.
        Accepts patterns like:
          ACTION: now
          ACTION: search: how to change careers
          ACTION: draft_checklist: Update my resume
        Returns (None, None) if not found.
        """
        if not response:
            return None, None
        upper = response.upper()
        idx = upper.find("ACTION:")
        if idx == -1:
            return None, None
        tail = response[idx + len("ACTION:"):].strip()
        # stop at ANSWER if present
        ans_idx = tail.upper().find("ANSWER:")
        if ans_idx != -1:
            tail = tail[:ans_idx].strip()
        if not tail:
            return None, None
        if ":" in tail:
            name, arg = tail.split(":", 1)
            return name.strip(), arg.strip()
        parts = tail.split(None, 1)
        name = parts[0].strip()
        arg = parts[1].strip() if len(parts) > 1 else ""
        return name, arg

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