.PHONY: help all install install-dev install-plot install-dev-plot install-prod test test-cov test-integration lint format format-check docs docs-serve clean build pre-commit-install pre-commit-run examples shell update
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

all: format lint test-cov build ## Run format, lint, tests (with coverage), and build

install: ## Install the package in development mode (without plot/visualization)
	poetry install

install-dev: ## Install with dev dependencies (tests, linting, docs)
	poetry install --with=dev

install-plot: ## Install with plot/visualization support
	poetry install -E plot

install-dev-plot: ## Install with dev dependencies AND plot/visualization support
	poetry install --with=dev -E plot

install-prod: ## Install only production dependencies (minimal)
	poetry install --only=main

test: ## Run the test suite
	poetry run pytest tests/ -v

test-cov: ## Run tests with coverage
	poetry run pytest tests/ -v --cov=soilprofilecollection --cov-report=html --cov-report=term-missing

test-integration: ## Run integration tests (if any)
	@echo "No integration tests defined for soilprofilecollection"

lint: ## Run linting checks
	poetry run ruff check soilprofilecollection/ tests/
	poetry run mypy soilprofilecollection --ignore-missing-imports

format: ## Format code
	poetry run ruff format soilprofilecollection/ tests/

format-check: ## Check code formatting without making changes
	poetry run ruff format --check soilprofilecollection/ tests/

docs: ## Build documentation with MkDocs
	poetry run mkdocs build

docs-serve: ## Serve documentation with MkDocs and watch for changes
	poetry run mkdocs serve

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	poetry build

pre-commit-install: ## Install pre-commit hooks
	poetry run pre-commit install

pre-commit-run: ## Run pre-commit on all files
	poetry run pre-commit run --all-files

examples: ## Run example scripts (basic functionality test)
	@echo "Testing basic examples..."
	@poetry run python -c "import soilprofilecollection; print('✓ Package imports successfully')"
	@poetry run python -c "from soilprofilecollection import SoilProfileCollection; print('✓ SoilProfileCollection imports successfully')"
	@python -c "import matplotlib" 2>/dev/null && echo "✓ Matplotlib is installed (plotting available)" || echo "ℹ Matplotlib not installed (install with: make install-plot)"
	@echo "✓ All examples completed successfully"

shell: ## Start a Poetry shell
	poetry shell

update: ## Update dependencies
	poetry update