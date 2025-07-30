from app.memory.hybrid_memory import HybridMemory

class LifeCoachAgent:
    def __init__(self, model):
        self.model = model  # injected model (OpenAIModel, etc.)
        self.memory = HybridMemory()

    def chat(self, user_input, metadata=None):
      context = self.memory.get_context(user_input, where={"source": "chat", **(metadata or {})})
      response = self.model.generate(context, user_input)
      self.memory.save(user_input, response, metadata=metadata)
      return response