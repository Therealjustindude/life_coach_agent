class ConversationBuffer:
    def __init__(self, max_messages=10):
        self.buffer = []
        self.max_messages = max_messages

    def add(self, role, content):
        self.buffer.append({"role": role, "content": content})
        if len(self.buffer) > self.max_messages:
            self.buffer.pop(0)

    def get_context(self):
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.buffer])