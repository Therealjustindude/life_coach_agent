import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv();

class BaseModel:
	def chat(self, messages: list[dict]) -> str:
		raise NotImplementedError

class OpenAIModel(BaseModel):
	def __init__(self, model="gpt-4o-mini"):
		self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
		self.model = model

	def chat(self, messages: list[dict]) -> str:
		response = self.client.chat.completions.create(
			model = self.model,
			messages = messages
		)
		return response.choices[0].message.content