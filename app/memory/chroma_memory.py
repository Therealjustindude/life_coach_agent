import chromadb
import datetime
import os

class ChromaMemory:
    def __init__(self, host="chroma", port=8000, default_metadata=None):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(name="life_coach_memory")
        
        # Auto-detect environment, default to "dev" if not set
        mode = os.getenv("APP_MODE", "dev")
        self.default_metadata = default_metadata or {
            "source": "chat",
            "environment": mode,
            "created_at": datetime.datetime.utcnow().isoformat()
        }

    def save_context(self, text: str, metadata=None):
        from uuid import uuid4
        doc_id = str(uuid4())
        if not metadata:
            metadata = {"source": "chat", "timestamp": datetime.datetime.utcnow().isoformat()}
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def query(self, query_text: str, n_results=5):
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return results.get("documents", [[]])[0]