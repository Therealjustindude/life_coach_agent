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
	     -d '{"message": "Hi coach", "user_id": "u1"}'
	```
3. **Test Actions with tools:**
	```bash
	curl -X POST http://localhost:8080/chat \
			-H "Content-Type: application/json" \
			-d '{"message":"What time is it right now, and make me a quick checklist to prep my resume", "user_id":"u1"}'
	```

- **AI life coaching**: Ask questions about career, life balance, and personal growth.
- **Hybrid memory**: Short-term conversation buffer + Chroma vector DB for semantic recall.
- **Structured prompting**: Uses a PromptBuilder module to combine system role, context, and user input for consistent, coach-like responses.
- **Extensible**: Swap models (OpenAI ↔ Ollama), add tools (job search, calendar), or upgrade memory.
- **API-first**: Interact over REST (ideal for frontends, bots, integrations).
- **Agent reasoning logs**: ReAct-style responses include `THOUGHT`, `ACTION`, and `ANSWER`. These are stored separately for auditing, debugging, or improvement.  
  _When adding new tools, update the ReAct format guide in the prompt template so the model knows available tool names, arguments, and when to use them._
- **Logging**: The agent logs reasoning and metadata to the console. In the future, this can be routed to external monitoring services.

## Reasoning Logs

Every response includes structured reasoning:
- **THOUGHT**: The agent’s internal reasoning
- **ACTION**: Any tools or external steps the agent considered
- **ANSWER**: The final message sent back to the user

These are stored in a separate memory collection (`ReasoningMemory`) and can be queried for analysis or performance monitoring.

## Architecture (High Level)

- **FastAPI service** → `/chat` endpoint
- **LifeCoachAgent** → orchestrates prompting, model calls, logging, and memory writes
- **ReactPromptBuilder** → fixed ReAct format (THOUGHT, ACTION, ANSWER) with swappable system prompt and optional examples
- **HybridMemory** → short-term buffer + Chroma vector DB (scoped by `user_id`)
- **ReasoningMemory** → separate Chroma collection for full reasoning traces (queryable)
- **OpenAIModel** → current model backend (GPT‑4o‑mini)

## Environment Variables

| Name                 | Purpose                                                        | Default    |
|----------------------|----------------------------------------------------------------|------------|
| `OPENAI_API_KEY`     | API key for OpenAI model                                       | (required) |
| `APP_MODE`           | App mode (`dev` or `prod`)                                     | `dev`      |
| `SHOW_AGENT_THOUGHTS`| Show THOUGHT/ACTION in API response (`true`/`false`)           | `false`    |
| `CHROMA_HOST`        | Chroma DB host                                                 | `chroma`   |
| `CHROMA_PORT`        | Chroma DB port                                                 | `8000`     |
| `COACH_STYLE`        | Prompt style (`default`, `cheerful`, `direct`, …)              | `default`  |
| `INCLUDE_EXAMPLES`   | Include few‑shot examples in prompts (`true`/`false`)          | `true`     |

> **Tip:** In dev you can experiment by changing `COACH_STYLE` and `INCLUDE_EXAMPLES` without code edits.

## Dev Tips

- Set `APP_MODE=dev` in `.env` for development behavior and metadata tagging.
- Keep `SHOW_AGENT_THOUGHTS=false` for users; enable `true` only for debugging.
- Tune prompt behavior via `COACH_STYLE` and `INCLUDE_EXAMPLES`.
- Whenever you add or rename tools in `ToolRegistry`, also update the `REACT_FORMAT_GUIDE` in `template.py` (or wherever your prompt template is stored) so the model is aware of the tool names and their expected usage format.

### Upcoming Priorities:
- 📋 Keep prompt template in sync with available tools (update tool list and usage examples in format guide).
- 🔍 Set up logging and monitoring for production (e.g. Sentry, Logtail, or similar service).
- 🤖 Continue to Build out multi-step reasoning with tool execution (full ReAct loop).
- 🧠 Improve agent quality (context window, prompt engineering, fallback logic).
- 🧪 Add tests for memory saving, prompt building, and response generation.
- 📦 Refactor and modularize memory classes for easier expansion.
- 🌐 Add auth + user signup (optional, for multi-user UI integration).
- 🚀 Prepare cloud-ready Docker setup for deployment to Fly.io, Render, or AWS.