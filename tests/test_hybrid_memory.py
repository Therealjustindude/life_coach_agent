from types import SimpleNamespace
from app.memory.hybrid_memory import HybridMemory

class StubBuffer:
    def __init__(self):
        self.history = [("u1","a1"),("u2","a2"),("u3","a3")]
    def get_last_n(self, n):
        pairs = self.history[-n:]
        lines=[]
        for u,a in pairs:
            lines += [f"User: {u}", f"Assistant: {a}"]
        return lines

class StubVector:
    def __init__(self, docs): self.docs = docs
    @property
    def collection(self):
        return SimpleNamespace(query=lambda **kw: {"documents":[self.docs]})

def test_get_context_blends_recent_and_semantic():
    buf = StubBuffer()
    vec = StubVector(docs=["memo1","memo2"])
    mem = HybridMemory(buffer=buf, vector_store=vec)
    ctx = mem.get_context("q", limit=2, top_k=2, summarize_threshold=10_000, summarize_fn=None)
    assert "Recent conversation:" in ctx and "Relevant past info:" in ctx
    assert "memo1" in ctx and "u2" in ctx  # last 2 exchanges present