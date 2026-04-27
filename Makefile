.PHONY: dev dev-core dev-agent dev-web build up down logs test lint clean help

# ─── Development ─────────────────────────────────────────────────

dev: ## Start all services in development mode
	@echo "🐦 Starting OpenSparrow in dev mode..."
	docker compose -f deploy/docker-compose.dev.yml up --build

dev-core: ## Start control plane only
	cd sparrow-core && pip install -e ".[dev]" && uvicorn sparrow.main:app --reload --port 8080

dev-agent: ## Start local agent only
	cd sparrow-agent && pip install -e ".[dev]" && sparrow-agent --core-url ws://localhost:8081/ws/agent

dev-web: ## Start frontend dev server
	cd sparrow-web && npm install && npm run dev

# ─── Production ──────────────────────────────────────────────────

build: ## Build all Docker images
	docker compose -f deploy/docker-compose.yml build

up: ## Start production services
	docker compose -f deploy/docker-compose.yml up -d
	@echo "🐦 OpenSparrow is running at http://localhost:3000"

down: ## Stop all services
	docker compose -f deploy/docker-compose.yml down

logs: ## Tail service logs
	docker compose -f deploy/docker-compose.yml logs -f

# ─── Testing ─────────────────────────────────────────────────────

test: ## Run all tests
	cd sparrow-core && python -m pytest tests/ -v
	cd sparrow-agent && python -m pytest tests/ -v

lint: ## Run linters
	cd sparrow-core && ruff check sparrow/
	cd sparrow-agent && ruff check agent/

# ─── Utilities ───────────────────────────────────────────────────

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf sparrow-web/dist sparrow-web/node_modules

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
