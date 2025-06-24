#!/usr/bin/env -S uv run
SHELL:=/usr/bin/bash
## VIRTUAL_ENV:=.civis  ## Optional if you want to use it.


##@ Utility
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: venv
venv: uv
	uv venv --python 3.12.3; \

.PHONY: uv
uv:  ## Install uv if it's not present.
	@command -v uv > /dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv --version

.PHONY: dev
dev: uv ## Install dev dependencies
	uv sync --test --active; \

ai: uv
	uv sync --ai --active;

.PHONY: lock
lock: uv ## lock dependencies
	uv lock

.PHONY: install
install: uv ## Install dependencies
	uv sync --all-groups --active;

.PHONY: test
test:  ## Run tests
	uv run pytest --active

.PHONY: lint
lint:  ## Run linters
	uv run ruff check ./src ./tests
	uv run ruff format ./src ./tests

.PHONY: cov
cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing --active