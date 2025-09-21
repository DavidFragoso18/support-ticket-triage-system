# -------- Settings --------
BACKEND_DIR := backend
APP_MODULE  := app.main:app
PORT        := 8000
PYTHON      := $(BACKEND_DIR)/.venv/Scripts/python.exe

.PHONY: help up down logs db lint test

help:
	@echo "make up     - Start Postgres (Docker) + run FastAPI (dev)"
	@echo "make down   - Stop & remove the Postgres container"
	@echo "make logs   - Tail Postgres logs"
	@echo "make db     - psql into the triage DB"
	@echo "make lint   - Ruff + Black check (if installed)"
	@echo "make test   - Run pytest (if present)"

up:
	@echo ">> Starting Postgres (Docker)…"
	-@docker start triage-pg >/dev/null 2>&1 || docker run --name triage-pg \
		-e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=triage \
		-p 5432:5432 -d postgres:16
	@echo ">> Running FastAPI (http://localhost:8000)…"
	cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn $(APP_MODULE) --reload --port $(PORT)

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
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest -q
