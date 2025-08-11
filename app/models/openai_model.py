from openai import OpenAI
import os
from app.models.base_model import BaseModel
from app.utils.get_env import get_env

class OpenAIModel(BaseModel):
    def __init__(self, model="gpt-5-mini"):
        self.client = OpenAI(api_key=get_env("OPENAI_API_KEY"))
        self.model = model

    def generate(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()