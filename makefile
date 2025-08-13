# Makefile for Life Coach Agent project

COMPOSE = docker compose

# Build and start containers
up:
	$(COMPOSE) up --build -d

# Start containers without rebuilding
start:
	$(COMPOSE) up -d

# Stop containers (keeps volumes/data)
stop:
	$(COMPOSE) stop

# Restart containers without rebuilding
restart:
	$(COMPOSE) restart

# Rebuild and restart containers
rebuild:
	$(COMPOSE) up --build -d

# Tear down containers and remove volumes (⚠️ wipes Chroma data)
reset:
	$(COMPOSE) down -v

# View logs (follow mode)
logs:
	$(COMPOSE) logs -f

# Exec into the agent container
shell-agent:
	$(COMPOSE) exec agent /bin/bash

# Exec into the chroma container
shell-chroma:
	$(COMPOSE) exec chroma /bin/bash

test:
	@echo "Running pytest..."
	docker compose run --rm -e PYTHONPATH=/app agent pytest -v