from typing import List, Tuple

class ConversationBufferMemory:
    def __init__(self):
        self.history: List[Tuple[str, str]] = []  # [(user, assistant)]

    def add(self, user: str, assistant: str):
        self.history.append((user, assistant))

    def get_all(self) -> List[str]:
        lines = []
        for u, a in self.history:
            lines.append(f"User: {u}")
            lines.append(f"Assistant: {a}")
        return lines

    # NEW
    def get_last_n(self, n: int) -> List[str]:
        if n <= 0 or not self.history:
            return []
        tail = self.history[-n:]
        lines = []
        for u, a in tail:
            lines.append(f"User: {u}")
            lines.append(f"Assistant: {a}")
        return lines