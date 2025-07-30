class BaseModel:
    def generate(self, context: str, user_input: str) -> str:
        """Generate a response based on context and user input."""
        raise NotImplementedError