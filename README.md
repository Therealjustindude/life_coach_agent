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
	     -d '{"message": "Give me some career advice"}'
	```

**Request Body Parameters:**

- `message` (string, required): The prompt or question for the life coach agent.
- `metadata` (object, optional): A JSON object containing additional context tags for the conversation.  
  Useful for multi-user support and filtering in the vector database. Example keys:  
  - `user_id`: Unique identifier for the user  
  - `session_id`: Identifier for the conversation session  
  - `topic`: Tag for categorizing the conversation

**Example with Metadata:**
	
	```bash
	curl -X POST http://localhost:8000/chat \
			-H "Content-Type: application/json" \
			-d '{
						"message": "Help me plan my week",
						"metadata": {"user_id": "u1", "session_id": "s1", "topic": "planning"}
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
	     -d '{"message": "Give me some career advice"}'
	```
	

## Features
- **AI life coaching**: Ask questions about career, life balance, and personal growth.
- **Hybrid memory**: Short-term conversation buffer + Chroma vector DB for semantic recall.
- **Extensible**: Swap models (OpenAI ↔ Ollama), add tools (job search, calendar), or upgrade memory.
- **API-first**: Interact over REST (ideal for frontends, bots, integrations).

## Next Steps:
- Add multi-step reasoning (ReAct-style).
- Add integrations (calendar, job search).
- Enhance deployment (cloud-ready configs, scaling).