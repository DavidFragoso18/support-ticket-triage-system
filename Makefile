# -------- Settings --------
BACKEND_DIR := backend
APP_MODULE  := app.main:app
PORT        := 8000


# Use the project's venv Python (Windows path). On macOS/Linux, change to: $(BACKEND_DIR)/.venv/bin/python
PYTHON := "backend/.venv/Scripts/python.exe"

.PHONY: help up up-db up-api down logs db lint test which-python seed-kb seed-resolutions seed seed-tickets

help:
	@echo "make up       - Start DB + API (dev)"
	@echo "make up-db    - Start Postgres only"
	@echo "make up-api   - Start FastAPI only (uses venv python)"
	@echo "make down     - Stop & remove the Postgres container"
	@echo "make logs     - Tail Postgres logs"
	@echo "make db       - psql into triage DB"
	@echo "make lint     - Ruff + Black check"
	@echo "make test     - Run pytest"
	@echo "make which-python - Show which Python is used"

up: up-db up-api

up-db:
	@echo "Starting Postgres..."
	-@docker start triage-pg >/dev/null 2>&1 || docker run --name triage-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=triage -p 5432:5432 -d postgres:16

up-api:
	@echo "Starting FastAPI on http://localhost:8000 ..."
	$(PYTHON) -m uvicorn $(APP_MODULE) --reload --port $(PORT) --app-dir $(BACKEND_DIR)

down:
	-@docker stop triage-pg
	-@docker rm triage-pg

logs:
	docker logs -f triage-pg

db:
	docker exec -it triage-pg psql -U postgres -d triage

lint:
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff check . && $(PYTHON) -m black --check .

test:
	$(PYTHON) -m pytest -q --rootdir=$(BACKEND_DIR)

which-python:
	@echo "Using Python:" && $(PYTHON) -c "import sys,platform; print(sys.executable); print(platform.python_version())"



seed:
	@echo "Seeding KB articles from data/seeds/kb_articles.csv ..."
	$(PYTHON) -m app.scripts.seed_kb
	@echo "Seeding tickets from data/seeds/tickets ..."
	$(PYTHON) -m app.scripts.seed_tickets
	@echo "Seeding resolutions from data/seeds/resolutions ..."
	$(PYTHON) -m app.scripts.seed_resolutions
	

seed-kb:
	@echo "Seeding KB articles from data/seeds/kb_articles.csv ..."
	$(PYTHON) -m app.scripts.seed_kb
	
	
seed-resolutions:
	@echo "Seeding resolutions from data/seeds/resolutions ..."
	$(PYTHON) -m app.scripts.seed_resolutions
	
seed-tickets:
	@echo "Seeding tickets from data/seeds/tickets ..."
	$(PYTHON) -m app.scripts.seed_tickets