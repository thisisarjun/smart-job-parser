
.PHONY: start start-dev test lint format clean pre-commit-install pre-commit-run pre-commit-all

setup:
	pip install -r requirements.txt
	pip install -r requirements.development.txt
	pre-commit install

# Pre-commit setup and commands
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run

pre-commit-all:
	pre-commit run --all-files

# Start the application in production mode
start:
	uvicorn src.main:app --host 0.0.0.0 --port 8000

# Start the application in development mode with auto-reload
start-dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests with coverage
test:
	pytest -v

# Run linting and type checking
lint:
	flake8 src tests
	mypy src tests

# Auto-fix linting issues where possible
lint-fix:
	black src tests
	isort src tests

# Format code (same as lint-fix for now)
format: lint-fix

# Run only flake8
lint-flake8:
	flake8 src tests

# Run only mypy
lint-mypy:
	mypy src tests

# Run all checks (lint + tests)
check: lint test

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
