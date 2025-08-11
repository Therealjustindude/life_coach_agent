from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.life_coach_agent import LifeCoachAgent
from app.models.openai_model import OpenAIModel
from app.utils.get_env import get_env
from fastapi.middleware.cors import CORSMiddleware


SHOW_THOUGHTS = get_env("SHOW_AGENT_THOUGHTS", "false").lower() == "true"
COACH_STYLE = get_env("COACH_STYLE", "default")
INCLUDE_EXAMPLES = get_env("INCLUDE_EXAMPLES", "true").lower() == "true"

app = FastAPI(title="Life Coach Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model + agent
model = OpenAIModel()
agent = LifeCoachAgent(
    model=model,
    coach_style=COACH_STYLE,
    include_examples=INCLUDE_EXAMPLES
)

class ChatRequest(BaseModel):
    message: str
    user_id: str  # Required user identifier
    metadata: dict | None = None  # Optional, defaults to None

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/version")
def version():
    return {"version": get_env("VERSION", "0.0.0")}

@app.post("/chat")
async def chat(request: ChatRequest):
    # Ensure user_id is always included in metadata for memory context
    metadata = request.metadata or {}
    metadata["user_id"] = request.user_id
    response = agent.chat(request.message, metadata=metadata)
    return {"response": response}