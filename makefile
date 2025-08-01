# Makefile for managing the CIVIS AI Policy Analyser backend

VENV_DIR = .venv

##@ Utility
.PHONY: help
help:  ## Show help for each command
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup

.PHONY: uv
uv:  ## Install uv if missing
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv --version

.PHONY: venv
venv: uv  ## Create virtual environment
	uv venv --python=python3.13 $(VENV_DIR)

.PHONY: install
install: uv  
	uv pip install .

.PHONY: setup
setup: clean venv install lock freeze  ## Full setup from scratch

.PHONY: lock
lock:  ## Lock dependencies
	uv lock

.PHONY: freeze
freeze:  ## Generate requirements.txt
	uv pip compile pyproject.toml -o requirements.txt

.PHONY: clean
clean:  ## Remove virtual environment
	rm -rf $(VENV_DIR)

##@ Lint & Test

.PHONY: test
test:  ## Run tests
	uv run pytest

.PHONY: cov
cov:  ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

.PHONY: lint
lint:  ## Run ruff lint
	uv run ruff check src tests

.PHONY: fix
fix:  ## Auto-fix lint and format issues
	uv run ruff check src tests --fix
	uv run ruff format src tests

##@ Run

.PHONY: run
run:  ## Run FastAPI server
	uv run uvicorn civis_backend_policy_analyser.api.app:app --reload

##@ Database

.PHONY: db-build
db-build:  ## Build DB Docker container
	docker compose build

.PHONY: db-up
db-up:  ## Start DB container
	docker compose up -d

.PHONY: db-down
db-down:  ## Stop DB container
	docker compose down

.PHONY: db-logs
db-logs:  ## Tail DB logs
	docker compose logs -f civis_postgres_container

.PHONY: db-psql
db-psql:  ## Open psql shell
	docker exec -it civis_postgres_container psql -U ffg -d civis

.PHONY: db-volume-clear
db-volume-clear: ## Warning: This will stop the DB container and remove the volume
	docker compose down
	docker volume rm draft-analyzer-be_pgdata || true
	@echo "✅ Database volume cleared"

##@ Data

.PHONY: seed
seed:  ## Seed data using existing environment
	@echo "Running seed_data.py using project environment..."
	uv run python seed_data.py
	@echo "✅ Seed completed"

.PHONY: quick-start
quick-start: setup db-up migrate seed run ## Full DB setup: install deps, run migrations, seed data
	@echo "✅ Full application started with sample database initialized"

.PHONY: migrate
migrate:
	@echo "Running migrations..."
	uv run alembic upgrade head

.PHONY: revision
revision:
	@echo "Creating new migration..."
	uv run alembic revision --autogenerate -m "Initial schema migration"
