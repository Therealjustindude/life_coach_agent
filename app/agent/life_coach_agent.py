from app.memory.hybrid_memory import HybridMemory
from app.agent.prompt_builder import PromptBuilder

class LifeCoachAgent:
    def __init__(self, model):
        self.model = model
        self.memory = HybridMemory()
        self.prompt_builder = PromptBuilder()

    def chat(self, user_input, metadata=None):
        context = self.memory.get_context(user_input, where={"user_id": metadata.get("user_id")})
        prompt = self.prompt_builder.build(
            context=context,
            user_input=user_input,
            extra_instructions=["Respond in a clear, structured way with next steps when possible."]
        )
        response = self.model.generate(prompt)
        self.memory.save(user_input, response, metadata=metadata)
        return response