from app.memory.chroma_memory import ChromaMemory
from app.memory.buffer_memory import ConversationBuffer

class HybridMemory:
    def __init__(self, buffer_size=10):
        self.buffer = ConversationBuffer(max_messages=buffer_size)
        self.vector_store = ChromaMemory()

    def save(self, user_input, assistant_response, metadata=None):
        self.buffer.add("User", user_input)
        self.buffer.add("Assistant", assistant_response)
        self.vector_store.save_context(
            f"User: {user_input}\nAssistant: {assistant_response}",
            metadata=metadata
        )

    def get_context(self, query, where=None):
        """
        Retrieve combined context: recent buffer + semantic search.
        Optionally filter semantic results by metadata using `where` dict.
        """
        if where is None:
            semantic_results = self.vector_store.query(query, n_results=5)
        else:
            raw_results = self.vector_store.collection.query(
                query_texts=[query],
                n_results=5,
                where=where
            )
            semantic_results = raw_results.get("documents", [[]])[0]

        buffer_context = self.buffer.get_context()

        return (
            "Recent conversation:\n"
            f"{buffer_context}\n\n"
            "Relevant past info:\n"
            f"{''.join(semantic_results)}"
        )