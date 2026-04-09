# ============================================================
#  Support Ticket Triage — Makefile
# ============================================================

# ---- Paths ----
BACKEND_DIR    := backend
FRONTEND_DIR   := frontend

# ---- Python (venv) ----
PYTHON         := $(BACKEND_DIR)/.venv/bin/python
PIP            := $(BACKEND_DIR)/.venv/bin/pip

# ---- App ----
APP_MODULE     := app.main:app
PORT           := 8000
FRONTEND_PORT  := 3000

# ---- Docker Compose ----
DOCKER         := /usr/local/bin/docker
DC             := $(DOCKER) compose
ENV_FILE       := .env

# ---- Ollama ----
OLLAMA_CONTAINER := ollama
OLLAMA_MODEL     := llama3.2:latest

.PHONY: help \
        up down deploy logs \
        up-backend up-frontend \
        up-ollama pull-model \
        setup \
        lint test \
        seed seed-kb seed-resolutions \
        clean

# ============================================================
#  HELP
# ============================================================
help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║           Support Ticket Triage — Commands           ║"
	@echo "╠══════════════════════════════════════════════════════╣"
	@echo "║  FULL STACK                                          ║"
	@echo "║    make up           Start all services (Docker)     ║"
	@echo "║    make down         Stop all services               ║"
	@echo "║    make deploy       Build images + start all        ║"
	@echo "║    make logs         Tail all container logs         ║"
	@echo "╠══════════════════════════════════════════════════════╣"
	@echo "║  INDIVIDUAL SERVICES                                 ║"
	@echo "║    make up-backend   Start only the backend          ║"
	@echo "║    make up-frontend  Start only the frontend         ║"
	@echo "║    make up-ollama    Start Ollama container + model  ║"
	@echo "╠══════════════════════════════════════════════════════╣"
	@echo "║  DEVELOPMENT                                         ║"
	@echo "║    make setup        Install all deps (venv + npm)   ║"
	@echo "║    make lint         Run ruff + black checks         ║"
	@echo "║    make test         Run all pytest tests            ║"
	@echo "╠══════════════════════════════════════════════════════╣"
	@echo "║  DATABASE                                            ║"
	@echo "║    make seed         Seed KB + resolutions           ║"
	@echo "║    make seed-kb      Seed KB articles only           ║"
	@echo "║    make seed-resolutions  Seed resolutions only      ║"
	@echo "╠══════════════════════════════════════════════════════╣"
	@echo "║  CLEANUP                                             ║"
	@echo "║    make clean        Stop + remove all volumes       ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	@echo ""

# ============================================================
#  FULL STACK  (Docker Compose)
# ============================================================

## Start all services (no rebuild)
up:
	@[ -f "$(ENV_FILE)" ] || cp .env.docker $(ENV_FILE)
	@echo "🐳 Starting all services..."
	$(DC) up -d
	@echo ""
	@echo "✅ All services running!"
	@echo "   Backend  → http://localhost:$(PORT)/docs"
	@echo "   Frontend → http://localhost:$(FRONTEND_PORT)"

## Stop all services
down:
	@echo "🛑 Stopping all services..."
	$(DC) down
	@echo "✅ Done."

## Build images and start everything
deploy:
	@[ -f "$(ENV_FILE)" ] || cp .env.docker $(ENV_FILE)
	@echo "🔨 Building images..."
	$(DC) build
	@echo "🚀 Deploying..."
	$(DC) up -d
	@echo ""
	@echo "✅ Deployment complete!"
	@echo "   Backend  → http://localhost:$(PORT)/docs"
	@echo "   Frontend → http://localhost:$(FRONTEND_PORT)"
	@echo "   Database → localhost:5432"

## Tail all container logs
logs:
	$(DC) logs -f

# ============================================================
#  INDIVIDUAL SERVICES
# ============================================================

## Start only the backend container
up-backend:
	@echo "🚀 Starting backend..."
	$(DC) up -d db redis backend
	@echo "✅ Backend running → http://localhost:$(PORT)/docs"

## Start only the frontend container
up-frontend:
	@echo "🚀 Starting frontend..."
	$(DC) up -d frontend
	@echo "✅ Frontend running → http://localhost:$(FRONTEND_PORT)"

## Start (or restart) the existing Ollama container, join the triage network, and ensure the model is present
up-ollama:
	@echo "🤖 Starting Ollama container..."
	$(DOCKER) start $(OLLAMA_CONTAINER)
	@echo "🔗 Connecting Ollama to triage network (safe to ignore if already connected)..."
	-$(DOCKER) network connect support-ticket-triage-system_triage-network $(OLLAMA_CONTAINER)
	@echo "📦 Pulling model $(OLLAMA_MODEL) (skipped if already present)..."
	$(DOCKER) exec $(OLLAMA_CONTAINER) ollama pull $(OLLAMA_MODEL)
	@echo "✅ Ollama is ready at http://localhost:11434"

# ============================================================
#  DEVELOPMENT  (local venv — no Docker for the app itself)
# ============================================================

## Install backend (venv) + frontend (npm) dependencies
setup:
	@echo "🚀 Setting up development environment..."
	@echo "1️⃣  Creating Python virtual environment..."
	cd $(BACKEND_DIR) && python3.11 -m venv .venv || python3 -m venv .venv
	@echo "2️⃣  Installing backend dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -e $(BACKEND_DIR)
	@echo "3️⃣  Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && npm install
	@echo ""
	@echo "✅ Setup complete!"
	@echo "   Run 'make up' to start all services with Docker."

## Run ruff linter + black formatter check
lint:
	@echo "🔍 Running linter..."
	$(PYTHON) -m ruff check $(BACKEND_DIR)
	$(PYTHON) -m black --check $(BACKEND_DIR)
	@echo "✅ Lint passed."

## Run all pytest tests (via Docker backend container)
test:
	@echo "🧪 Running tests..."
	$(DOCKER) exec -e PYTHONPATH=/app triage-backend pytest /app/tests/ -v --tb=short
	@echo "✅ Tests complete."

# ============================================================
#  DATABASE SEEDING
# ============================================================

seed: seed-kb seed-resolutions

seed-kb:
	@echo "🌱 Seeding KB articles..."
	cd $(BACKEND_DIR) && .venv/bin/python -m app.scripts.seed_kb
	@echo "✅ KB articles seeded."

seed-resolutions:
	@echo "🌱 Seeding resolutions..."
	cd $(BACKEND_DIR) && .venv/bin/python -m app.scripts.seed_resolutions
	@echo "✅ Resolutions seeded."

# ============================================================
#  CLEANUP
# ============================================================

## Stop all services and remove volumes (destructive)
clean:
	@echo "🗑️  Removing all containers and volumes..."
	$(DC) down -v
	@echo "✅ Cleanup done."
