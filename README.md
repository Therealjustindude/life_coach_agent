# Life Coach Agent

An AI-powered life coach that helps you plan your career, balance life, and stay accountable.  
Currently powered by OpenAI GPT-4o-mini, with support for local models (Ollama) coming soon.

---

## Setup

### Local Development (Dev Mode)

1. **Clone & enter project:**
	```bash
	git clone <repo_url>
	cd life_coach_agent
	```

2. **Create & activate a virtual environment:**
	```bash
	python3 -m venv venv
	source venv/bin/activate 
	```

3. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

4. **Set up environment variables:**
	```bash
	touch .env
	echo "OPENAI_API_KEY=your_key_here" >> .env
	```

5. **Run the FastAPI server locally with hot-reload:**
	```bash
	uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
	```

6. **Test the API:**
	```bash
	curl -X POST http://localhost:8000/chat \
	     -H "Content-Type: application/json" \
	     -d '{"message": "Give me some career advice", "user_id": "u1"}'
	```

**Request Body Parameters:**

- `message` (string, required): The prompt or question for the life coach agent.
- `user_id` (string, required): A unique identifier for the user. Ensures that memory and context are isolated per user.
- `metadata` (object, optional): A JSON object containing additional context tags for the conversation.  
  Useful for further filtering in the vector database. Example keys:  
  - `session_id`: Identifier for the conversation session  
  - `topic`: Tag for categorizing the conversation

**Example with Metadata:**

```bash
curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{
        "message": "Help me plan my week",
        "user_id": "u1",
        "metadata": {"session_id": "s1", "topic": "planning"}
    }'
```

Access interactive API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Running in Docker

1. **Build & run with Docker Compose:**
	```bash
	docker-compose up --build
	```

2. **Access the API:**
	```bash
	curl -X POST http://localhost:8080/chat \
	     -H "Content-Type: application/json" \
	     -d '{"message": "Give me some career advice", "user_id": "u1"}'
	```
	

## Features
- **AI life coaching**: Ask questions about career, life balance, and personal growth.
- **Hybrid memory**: Short-term conversation buffer + Chroma vector DB for semantic recall.
- **Structured prompting**: Uses a PromptBuilder module to combine system role, context, and user input for consistent, coach-like responses.
- **Extensible**: Swap models (OpenAI ↔ Ollama), add tools (job search, calendar), or upgrade memory.
- **API-first**: Interact over REST (ideal for frontends, bots, integrations).
- **Agent reasoning logs**: ReAct-style responses include `THOUGHT`, `ACTION`, and `ANSWER`. These are stored separately for auditing, debugging, or improvement.
- **Logging**: The agent logs reasoning and metadata to the console. In the future, this can be routed to external monitoring services.

## Reasoning Logs

Every response includes structured reasoning:
- **THOUGHT**: The agent’s internal reasoning
- **ACTION**: Any tools or external steps the agent considered
- **ANSWER**: The final message sent back to the user

These are stored in a separate memory collection (`ReasoningMemory`) and can be queried for analysis or performance monitoring.

-### Dev Tips

- Set `APP_MODE=dev` in your `.env` file to include environment metadata and enable development-specific behavior.
- You can toggle visibility of internal `THOUGHT` output in API responses (via a feature flag in code).

## Next Steps:
- Add multi-step reasoning (ReAct-style for planning and reasoning).
- Add integrations (calendar, job search).
- Enhance deployment (cloud-ready configs, scaling).