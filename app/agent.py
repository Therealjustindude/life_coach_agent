from app.models import OpenAIModel
from app.memory import SimpleMemory

class LifeCoachAgent:
	def __init__(self, brain = None, memory = None):
		self.brain = brain or OpenAIModel()
		self.memory = memory or SimpleMemory()

	def get_advice(self, question: str) -> str:
		# Load past messages (short history)
			conversation = self.memory.get_conversation()
			messages = [{"role": "system", "content": "You are a thoughtful, practical, and encouraging life coach."}]
			messages.extend(conversation)
			messages.append({"role": "user", "content": question})

			# Get response
			response = self.brain.chat(messages)

			# Save both user + agent messages
			self.memory.add_message("user", question)
			self.memory.add_message("assistant", response)

			return response