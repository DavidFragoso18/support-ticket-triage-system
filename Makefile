# -------- Settings --------
BACKEND_DIR := backend
APP_MODULE  := app.main:app
PORT        := 8000

# DB settings
DB_CONTAINER := triage-pg
DB_IMAGE     := pgvector/pgvector:pg16   # <— pgvector-enabled Postgres
DB_NAME      := triage
DB_USER      := postgres
DB_PASS      := postgres
DB_PORT      := 5432
DB_VOLUME    := triage_pg_data

# Use the project's venv Python (Windows path). On macOS/Linux, use $(BACKEND_DIR)/.venv/bin/python
PYTHON := "backend/.venv/Scripts/python.exe"

.PHONY: help up up-db up-api down logs db lint test which-python seed seed-kb seed-resolutions seed-tickets

help:
	@echo "make up          - Start DB + API (dev)"
	@echo "make up-db       - Start Postgres (pgvector) only"
	@echo "make up-api      - Start FastAPI only (uses venv python)"
	@echo "make down        - Stop & remove the Postgres container"
	@echo "make logs        - Tail Postgres logs"
	@echo "make db          - psql into triage DB"
	@echo "make lint        - Ruff + Black check"
	@echo "make test        - Run pytest"
	@echo "make which-python- Show which Python is used"
	@echo "make seed        - Seed KB, tickets, resolutions"

up: up-db up-api

# Start pgvector-enabled Postgres; create a named volume so data persists
up-db:
	@echo "Starting Postgres (pgvector)..."
	-@docker volume create $(DB_VOLUME) >/dev/null
	-@docker start $(DB_CONTAINER) >/dev/null 2>&1 || docker run --name $(DB_CONTAINER) \
		-e POSTGRES_PASSWORD=$(DB_PASS) -e POSTGRES_USER=$(DB_USER) -e POSTGRES_DB=$(DB_NAME) \
		-p $(DB_PORT):5432 -v $(DB_VOLUME):/var/lib/postgresql/data -d $(DB_IMAGE)
	@echo "Ensuring pgvector extension exists..."
	-@docker exec -t $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "CREATE EXTENSION IF NOT EXISTS vector;" >/dev/null 2>&1 || true

up-api:
	@echo "Starting FastAPI on http://localhost:$(PORT) ..."
	$(PYTHON) -m uvicorn $(APP_MODULE) --reload --port $(PORT) --app-dir $(BACKEND_DIR)

down:
	-@docker stop $(DB_CONTAINER)
	-@docker rm $(DB_CONTAINER)

logs:
	docker logs -f $(DB_CONTAINER)

db:
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

lint:
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff check . && $(PYTHON) -m black --check .

test:
	$(PYTHON) -m pytest -q --rootdir=$(BACKEND_DIR)

which-python:
	@echo "Using Python:" && $(PYTHON) -c "import sys,platform; print(sys.executable); print(platform.python_version())"

# --- Seeding (run from backend/ to resolve 'app.*' modules reliably on Windows) ---
seed:
	@echo "Seeding KB articles from data/seeds/kb_articles.csv ..."
	cd $(BACKEND_DIR) && .\.venv\Scripts\python.exe -m app.scripts.seed_kb
	@echo "Seeding tickets from data/seeds/tickets ..."
	cd $(BACKEND_DIR) && .\.venv\Scripts\python.exe -m app.scripts.seed_tickets
	@echo "Seeding resolutions from data/seeds/resolutions ..."
	cd $(BACKEND_DIR) && .\.venv\Scripts\python.exe -m app.scripts.seed_resolutions
	@echo "✅ All seeds completed."

seed-kb:
	@echo "Seeding KB articles from data/seeds/kb_articles.csv ..."
	cd $(BACKEND_DIR) && .\.venv\Scripts\python.exe -m app.scripts.seed_kb

seed-resolutions:
	@echo "Seeding resolutions from data/seeds/resolutions.csv ..."
	cd $(BACKEND_DIR) && .\.venv\Scripts\python.exe -m app.scripts.seed_resolutions

seed-tickets:
	@echo "Seeding tickets from data/seeds/tickets ..."
	cd $(BACKEND_DIR) && .\.venv\Scripts\python.exe -m app.scripts.seed_tickets
