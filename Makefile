# -------- Settings --------
BACKEND_DIR := backend
FRONTEND_DIR := frontend
APP_MODULE  := app.main:app
PORT        := 8000
FRONTEND_PORT := 3000

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

.PHONY: help up up-db up-api down logs db lint test which-python seed seed-kb seed-resolutions seed-tickets deploy build-frontend start-frontend install-frontend

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
	@echo "make deploy      - Deploy full stack (DB + API + Frontend)"
	@echo "make build-frontend - Build frontend for production"
	@echo "make install-frontend - Install frontend dependencies"

up: up-db up-api

# Start pgvector-enabled Postgres; create a named volume so data persists
up-db:
	@echo "Starting Postgres (pgvector)..."
	-@docker volume create $(DB_VOLUME) >nul 2>&1
	-@docker stop $(DB_CONTAINER) >nul 2>&1
	-@docker rm $(DB_CONTAINER) >nul 2>&1
	@docker run --name $(DB_CONTAINER) \
		-e POSTGRES_PASSWORD=$(DB_PASS) -e POSTGRES_USER=$(DB_USER) -e POSTGRES_DB=$(DB_NAME) \
		-p $(DB_PORT):5432 -v $(DB_VOLUME):/var/lib/postgresql/data -d $(DB_IMAGE)
	@echo "Ensuring pgvector extension exists..."
	@powershell -Command "Start-Sleep -Seconds 3"
	-@docker exec -t $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "CREATE EXTENSION IF NOT EXISTS vector;" >nul 2>&1

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

# --- Frontend targets ---
install-frontend:
	@echo "Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && npm install

build-frontend:
	@echo "Building frontend for production..."
	cd $(FRONTEND_DIR) && npm run build

start-frontend:
	@echo "Starting frontend on http://localhost:$(FRONTEND_PORT) ..."
	cd $(FRONTEND_DIR) && npm run dev

# --- Deployment ---
deploy: up-db install-frontend build-frontend
	@echo "🚀 Deploying support ticket triage system..."
	@echo "1. Database is starting..."
	@powershell -Command "Start-Sleep -Seconds 5"
	@echo "2. Seeding database..."
	$(MAKE) seed
	@echo "3. Starting backend API..."
	@echo "   Backend will be available at http://localhost:$(PORT)"
	@echo "4. Frontend built and ready to serve"
	@echo "   To start frontend: make start-frontend"
	@echo "✅ Deployment complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  - Backend API: http://localhost:$(PORT)"
	@echo "  - Run 'make start-frontend' for frontend at http://localhost:$(FRONTEND_PORT)"
	@echo "  - Run 'make up-api' to start the backend server"
