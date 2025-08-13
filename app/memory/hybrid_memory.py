# hybrid_memory.py (essentials)
from typing import Optional, Callable, Dict, Any, List

class HybridMemory:
    def __init__(self, buffer, vector_store):
        self.buffer = buffer             # BufferMemory instance
        self.vector_store = vector_store # Chroma wrapper/collection

    def _join(self, header: str, lines: List[str]) -> str:
        body = "\n".join(lines) if lines else "(none)"
        return f"{header}\n{body}"

    def get_context(
        self,
        query: str,
        *,
        where: Optional[Dict[str, Any]] = None,
        limit: int = 8,
        top_k: int = 5,
        summarize_threshold: int = 1400,
        summarize_fn: Optional[Callable[[str], str]] = None,
    ) -> str:
        # 1) recent
        getter = getattr(self.buffer, "get_last_n", None)
        if callable(getter):
            recent_lines = getter(limit)
        else:
            recent_lines = self.buffer.get_all()
            
        recent_block = self._join("Recent conversation:", recent_lines)

        # 2) semantic
        sem_docs: List[str] = []
        try:
            res = self.vector_store.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=where or {},
            )
            sem_docs = res.get("documents", [[]])[0] if res else []
        except Exception:
            sem_docs = []
        sem_block = self._join("Relevant past info:", sem_docs)

        combined = f"{recent_block}\n\n{sem_block}".strip()

        # 3) auto-summarize if long
        if summarize_fn and len(combined) > summarize_threshold:
            prompt = (
                "Summarize the following prior conversation and notes into 5–7 crisp bullets. "
                "Preserve facts, goals, commitments, constraints, and dates.\n\n" + combined
            )
            try:
                summary = summarize_fn(prompt)
                return f"Summary of prior context:\n{summary.strip()}"
            except Exception:
                pass
        return combined

    def save(self, user_input: str, assistant_response: str, metadata: Optional[dict] = None):
        self.buffer.add(user_input, assistant_response)
        self.vector_store.save_context(
            f"User: {user_input}\nAssistant: {assistant_response}",
            metadata=metadata,
        )