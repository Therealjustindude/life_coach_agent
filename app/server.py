from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.life_coach_agent import LifeCoachAgent
from app.models.openai_model import OpenAIModel

app = FastAPI(title="Life Coach Agent API")

# Initialize model + agent
model = OpenAIModel()
agent = LifeCoachAgent(model)

class ChatRequest(BaseModel):
    message: str
    user_id: str  # Required user identifier
    metadata: dict | None = None  # Optional, defaults to None

@app.post("/chat")
async def chat(request: ChatRequest):
    # Ensure user_id is always included in metadata for memory context
    metadata = request.metadata or {}
    metadata["user_id"] = request.user_id
    response = agent.chat(request.message, metadata=metadata)
    return {"response": response}