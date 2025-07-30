from openai import OpenAI
import os
from app.models.base_model import BaseModel
from app.utils.get_env import get_env

class OpenAIModel(BaseModel):
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=get_env("OPENAI_API_KEY"))
        self.model = model

    def generate(self, context: str, user_input: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful life coach."},
            {"role": "system", "content": context},
            {"role": "user", "content": user_input}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content