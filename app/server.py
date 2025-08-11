from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.life_coach_agent import LifeCoachAgent
from app.models.openai_model import OpenAIModel
import os

SHOW_THOUGHTS = os.getenv("SHOW_AGENT_THOUGHTS", "false").lower() == "true"
COACH_STYLE = os.getenv("COACH_STYLE", "default")
INCLUDE_EXAMPLES = os.getenv("INCLUDE_EXAMPLES", "true").lower() == "true"

app = FastAPI(title="Life Coach Agent API")

# Initialize model + agent
model = OpenAIModel()
agent = LifeCoachAgent(
    model=OpenAIModel(),
    coach_style=COACH_STYLE,
    include_examples=INCLUDE_EXAMPLES
)

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