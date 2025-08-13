import os, uuid
from datetime import datetime, UTC
import chromadb
from app.utils.get_env import get_env


class ChromaMemory:
    def __init__(self, default_metadata=None):
        host = get_env("CHROMA_HOST", "chroma")
        port = int(get_env("CHROMA_PORT", "8000"))
        mode = get_env("APP_MODE", "dev")
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(name="chat_memory")
        self.default_metadata = default_metadata or {"source": "chat", "environment": mode}

    def save_context(self, text: str, metadata: dict | None = None):
        meta = {
            **self.default_metadata, 
            **(metadata or {}), 
            "created_at": datetime.now(UTC).isoformat()
        }
        self.collection.add(
            documents=[text],
            metadatas=[meta],
            ids=[str(uuid.uuid4())],
        )