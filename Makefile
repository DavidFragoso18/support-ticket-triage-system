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

# Use the project's venv Python (detect OS)
ifeq ($(OS),Windows_NT)
	PYTHON := backend/.venv/Scripts/python.exe
	PYTHON_LOCAL := .venv/Scripts/python.exe
else
	PYTHON := backend/.venv/bin/python
	PYTHON_LOCAL := .venv/bin/python
endif

# Docker Compose settings
DOCKER_COMPOSE := docker-compose
ENV_FILE := .env

.PHONY: help up up-local up-db up-api down down-db logs db lint test which-python seed seed-kb seed-resolutions seed-tickets deploy deploy-local build-frontend start-frontend install-frontend docker-up docker-down docker-logs docker-build docker-deploy docker-clean

help:
	@echo "=== Quick Commands (Docker Compose) ==="
	@echo "make up          - Start all services with Docker Compose"
	@echo "make down        - Stop all Docker Compose services"
	@echo "make deploy      - Build and deploy with Docker Compose"
	@echo ""
	@echo "=== Docker Compose ==="
	@echo "make docker-up   - Start all services"
	@echo "make docker-down - Stop all services"
	@echo "make docker-logs - View logs (all services)"
	@echo "make docker-build- Build Docker images"
	@echo "make docker-deploy - Build and deploy"
	@echo "make docker-clean- Stop and remove all (including volumes)"
	@echo ""
	@echo "=== Local Development (venv) ==="
	@echo "make up-local    - Start DB + API (dev with venv)"
	@echo "make up-db       - Start Postgres (pgvector) only"
	@echo "make up-api      - Start FastAPI only (uses venv python)"
	@echo "make down-db     - Stop local Postgres container"
	@echo ""
	@echo "=== Database ==="
	@echo "make db          - psql into triage DB"
	@echo "make seed        - Seed KB, tickets, resolutions"
	@echo ""
	@echo "=== Development ==="
	@echo "make logs        - Tail Postgres logs"
	@echo "make lint        - Ruff + Black check"
	@echo "make test        - Run pytest"
	@echo "make which-python- Show which Python is used"
	@echo ""
	@echo "=== Frontend ==="
	@echo "make build-frontend - Build frontend for production"
	@echo "make install-frontend - Install frontend dependencies"
	@echo ""
	@echo "=== Quick Commands ==="
	@echo "make deploy      - Deploy full stack with Docker Compose"

# Main targets (Docker Compose by default)
up: docker-up

down: docker-down

# Legacy local development targets
up-local: up-db up-api

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

down-db:
	@echo "Stopping local Postgres container..."
	-@docker stop $(DB_CONTAINER)
	-@docker rm $(DB_CONTAINER)
	@echo "✅ Database stopped!"

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

# --- Seeding (run from backend/ to resolve 'app.*' modules reliably) ---
seed:
	@echo "Seeding KB articles from data/seeds/kb_articles.csv ..."
	cd $(BACKEND_DIR) && $(PYTHON_LOCAL) -m app.scripts.seed_kb
	@echo "Seeding tickets from data/seeds/tickets ..."
	cd $(BACKEND_DIR) && $(PYTHON_LOCAL) -m app.scripts.seed_tickets
	@echo "Seeding resolutions from data/seeds/resolutions ..."
	cd $(BACKEND_DIR) && $(PYTHON_LOCAL) -m app.scripts.seed_resolutions
	@echo "✅ All seeds completed."

seed-kb:
	@echo "Seeding KB articles from data/seeds/kb_articles.csv ..."
	cd $(BACKEND_DIR) && $(PYTHON_LOCAL) -m app.scripts.seed_kb

seed-resolutions:
	@echo "Seeding resolutions from data/seeds/resolutions.csv ..."
	cd $(BACKEND_DIR) && $(PYTHON_LOCAL) -m app.scripts.seed_resolutions

seed-tickets:
	@echo "Seeding tickets from data/seeds/tickets ..."
	cd $(BACKEND_DIR) && $(PYTHON_LOCAL) -m app.scripts.seed_tickets

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

# --- Docker Compose Commands ---
docker-up:
	@echo "🐳 Starting all services with Docker Compose..."
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "📝 Creating .env from .env.docker..."; \
		cp .env.docker .env; \
	fi
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Services started!"
	@echo ""
	@echo "Access URLs:"
	@echo "  Backend API: http://localhost:8000/docs"
	@echo "  Frontend: http://localhost:3000"
	@echo ""
	@echo "View logs: make docker-logs"

docker-down:
	@echo "🛑 Stopping all Docker Compose services..."
	$(DOCKER_COMPOSE) down
	@echo "✅ Services stopped!"

docker-logs:
	@echo "📋 Viewing Docker Compose logs (Ctrl+C to exit)..."
	$(DOCKER_COMPOSE) logs -f

docker-build:
	@echo "🔨 Building Docker images..."
	$(DOCKER_COMPOSE) build
	@echo "✅ Build complete!"

docker-deploy: docker-build
	@echo "🚀 Deploying with Docker Compose..."
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "📝 Creating .env from .env.docker..."; \
		cp .env.docker .env; \
	fi
	$(DOCKER_COMPOSE) up -d
	@echo ""
	@echo "⏳ Waiting for services to start (30 seconds)..."
	@sleep 30
	@echo ""
	@echo "✅ Deployment complete!"
	@echo ""
	@echo "Access URLs:"
	@echo "  Backend API: http://localhost:8000/docs"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Database: localhost:5432"
	@echo ""
	@echo "Useful commands:"
	@echo "  make docker-logs  - View logs"
	@echo "  make docker-down  - Stop services"
	@echo "  make seed         - Seed database"

docker-clean:
	@echo "🗑️  Cleaning up Docker Compose resources..."
	$(DOCKER_COMPOSE) down -v
	@echo "✅ Cleanup complete!"

# --- Deployment (Docker Compose) ---
deploy: docker-deploy

# Legacy local deployment
deploy-local: up-db install-frontend build-frontend
	@echo "🚀 Deploying support ticket triage system (local dev)..."
	@echo "1. Database is starting..."
	@sleep 5
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
