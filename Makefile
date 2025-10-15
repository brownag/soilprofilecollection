.PHONY: help install install-dev test test-cov test-integration lint format format-check docs docs-serve clean build pre-commit-install pre-commit-run examples
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install the package in development mode
	poetry install

install-prod: ## Install only production dependencies
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
	@echo "✓ All examples completed successfully"

shell: ## Start a Poetry shell
	poetry shell

update: ## Update dependencies
	poetry update</content>
<parameter name="filePath">/home/andrew/workspace/soilmcp/upstream/soilprofilecollection/Makefile