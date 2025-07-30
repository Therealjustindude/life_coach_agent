from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import LifeCoachAgent
from app.models.openai_model import OpenAIModel

app = FastAPI(title="Life Coach Agent API")

# Initialize model + agent
model = OpenAIModel()
agent = LifeCoachAgent(model)

class ChatRequest(BaseModel):
    message: str
    metadata: dict | None = None  # Optional, defaults to None

@app.post("/chat")
async def chat(request: ChatRequest):
    response = agent.chat(request.message, metadata=request.metadata)
    return {"response": response}