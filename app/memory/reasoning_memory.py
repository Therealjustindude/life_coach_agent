import chromadb
import datetime
from uuid import uuid4
from app.utils.get_env import get_env

class ReasoningMemory:
	def __init__(self):
		host = get_env("CHROMA_HOST", "chroma")
		port = int(get_env("CHROMA_PORT", "8000"))
		self.client = chromadb.HttpClient(host=host, port=port)
		self.collection = self.client.get_or_create_collection(name="reasoning_memory")

	def save(self, raw_response: str, user_id: str, session_id: str = None, topic: str = None):
		"""
		Save full reasoning (THOUGHT/ACTION/ANSWER) to chroma with metadata.
		"""
		doc_id = str(uuid4())
		metadata = {
			"user_id": user_id,
			"session_id": session_id or "default",
			"topic": topic or "general",
			"created_at": datetime.datetime.utcnow().isoformat()
		}
		self.collection.add(
			documents=[raw_response],
			metadatas=[metadata],
			ids=[doc_id]
		)

	def query(self, query_text: str, user_id: str = None, session_id: str = None, n_results=5):
		"""
		Search reasoning logs by text and optional filters (user/session).
		"""
		where = {}
		if user_id:
			where["user_id"] = user_id
		if session_id:
			where["session_id"] = session_id

		results = self.collection.query(
			query_texts=[query_text],
			n_results=n_results,
			where=where if where else None
		)
		return results.get("documents", [[]])[0]