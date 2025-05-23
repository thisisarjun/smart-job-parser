.PHONY: start start-dev test lint format clean

# Start the application in production mode
start:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

# Start the application in development mode with auto-reload
start-dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests with coverage
test:
	pytest

# Run linting and type checking
lint:
	flake8 .
	mypy .

# Format code
format:
	black .
	isort .

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