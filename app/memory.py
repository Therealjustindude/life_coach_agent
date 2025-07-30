import json
import os

class SimpleMemory:
	def __init__(self, filepath="memory.json"):
		self.filepath = filepath
		self.data = self._load()

	def _load(self):
		if os.path.exists(self.filepath):
			with open(self.filepath, "r") as f:
				return json.load(f)
		return {"conversations": []}

	def save(self):
		with open(self.filepath, "w") as f:
			json.dump(self.data, f, indent = 2)

	def add_message(self, role, content):
		self.data["conversations"].append({"role": role, "content": content})
		self.save()
	
	def get_conversation(self, limit=10):
		return self.data["conversations"][-limit:]