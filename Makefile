.PHONY: help install dev-install check-deps setup build up down down-v logs clean format lint run-local doctor migrate rebuild prune

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

check-deps: ## Check and prompt installation of required dependencies
	@echo "Checking dependencies..."
	@command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Install it from https://www.python.org/"; exit 1; }
	@command -v uv >/dev/null 2>&1 || { echo "uv is required but not installed. Install it from https://docs.astral.sh/uv/getting-started/installation/"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Install it from https://www.docker.com/"; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed."; exit 1; }
	@command -v psql >/dev/null 2>&1 || echo "Warning: psql (PostgreSQL client) not found. It's recommended for database operations."
	@echo "All required dependencies are installed!"

install: check-deps ## Install production dependencies with uv
	uv sync --no-dev

dev-install: check-deps ## Install development dependencies with uv
	uv sync

setup: check-deps ## Setup project (install deps and create .env)
	@echo "Setting up project..."
	@$(MAKE) dev-install
	@if [ ! -f .env ]; then \
		echo "Creating .env file from env.example..."; \
		cp env.example .env 2>/dev/null || echo "Note: env.example not found, create .env manually"; \
	fi
	@echo "Setup complete!"

build: ## Build Docker images
	docker compose build

up: ## Start all services with Docker Compose
	docker compose up -d
	@echo "Services are starting..."
	@echo "API will be available at http://localhost:8000"
	@echo "API docs at http://localhost:8000/docs"

down: ## Stop all services
	docker compose down

down-v: ## Stop all services and remove volumes
	docker compose down -v

logs: ## Show logs from all services
	docker compose logs -f

logs-app: ## Show logs from app service
	docker compose logs -f app


clean: ## Clean up generated files and containers
	docker compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .venv 2>/dev/null || true
	@echo "Cleanup complete!"

format: ## Format code with black and isort using uv
	uv run black app/
	uv run isort app/

lint: ## Lint code with flake8 using uv
	uv run flake8 app/ --max-line-length=100 --exclude=__pycache__

shell: ## Open shell in app container
	docker compose exec app /bin/sh

db-shell: ## Open PostgreSQL shell
	docker compose exec db psql -U postgres -d auth_db

migrate-create: ## Create new migration (usage: make migrate-create name=migration_name)
	@if [ -z "$(name)" ]; then \
		echo "Error: migration name required. Usage: make migrate-create name=migration_name"; \
		exit 1; \
	fi
	uv run alembic revision --autogenerate -m "$(name)"

migrate-up: ## Apply migrations
	uv run alembic upgrade head

migrate-down: ## Rollback last migration
	uv run alembic downgrade -1

migrate: migrate-up ## Shortcut alias for migrations

run-local: ## Run app locally without Docker (no reload)
	uv run uvicorn main:app --host 0.0.0.0 --port 8000

run-dev: ## Run application in development mode with auto-reload
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev: up ## Start development environment (alias for up)
	@echo "Development environment is ready!"
	@echo "Access the API at http://localhost:8000"
	@echo "Access the docs at http://localhost:8000/docs"

rebuild: down-v build up ## Full rebuild (clean + build + up)
	@echo "♻️  Environment rebuilt successfully."

status: ## Show status of all services
	docker compose ps

restart: ## Restart all services
	docker compose restart

health: ## Check health of the application
	@curl -s http://localhost:8000/health | python3 -m json.tool || echo "Service is not running or not healthy"

# Authentication specific commands
test-auth: ## Test authentication endpoints
	@echo "Testing authentication endpoints..."
	@echo "1. Testing registration..."
	@curl -s -X POST http://localhost:8000/auth/register \
		-H "Content-Type: application/json" \
		-d '{"email": "test@example.com", "password": "testpass123", "full_name": "Test User"}' | python3 -m json.tool || echo "Registration failed"

test-google-oauth: ## Test Google OAuth flow
	@echo "Testing Google OAuth..."
	@curl -s http://localhost:8000/auth/google | python3 -m json.tool || echo "Google OAuth failed"

# Database management
db-reset: ## Reset database (WARNING: This will delete all data!)
	@echo "WARNING: This will delete all data in the database!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ] || exit 1
	docker compose down -v
	docker compose up -d db
	sleep 5
	$(MAKE) migrate-up

# Development helpers
install-deps: ## Install/update dependencies
	uv sync

check-env: ## Check environment configuration
	@echo "Checking environment configuration..."
	@if [ -f .env ]; then \
		echo "✅ .env file exists"; \
		echo "📋 Current configuration:"; \
		grep -E "^[A-Z_]+=" .env | head -10; \
	else \
		echo "❌ .env file not found. Run 'make setup' to create it."; \
	fi

doctor: ## Run full environment diagnostics
	@$(MAKE) check-deps
	@$(MAKE) check-env
	@echo "✅ Everything looks good! Ready for development 🚀"

prune: ## Remove all unused Docker data (⚠️ dangerous)
	docker system prune -af --volumes

