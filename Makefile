.PHONY: build run stop clean test lint install

# Docker compose commands
build:
	docker compose build

# build the frontend docker image
build-frontend:
	docker compose build frontend --no-cache

# build the api docker image
build-api:
	docker compose build api --no-cache

run:
	docker compose up -d

stop:
	docker compose down

# Development setup
install:
	cd api && poetry install
	cd frontend && npm install

# Testing
test-api:
	cd api && poetry run pytest

test-frontend:
	cd frontend && npm test

test: test-api test-frontend

# Linting
lint-api:
	cd api && poetry run black .
	cd api && poetry run flake8

lint-frontend:
	cd frontend && npm run lint

lint: lint-api lint-frontend

log:
	docker compose logs -f

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name ".venv" -exec rm -rf {} +
	find . -type f -name "poetry.lock" -delete
	find . -type f -name "package-lock.json" -delete

# Development servers
dev-api:
	cd api && poetry run python app.py

dev-frontend:
	cd frontend && npm run dev

# Help
help:
	@echo "Available commands:"
	@echo "  build         - Build Docker images"
	@echo "  run           - Run the application in Docker"
	@echo "  stop          - Stop Docker containers"
	@echo "  install       - Install dependencies for local development"
	@echo "  test          - Run all tests"
	@echo "  test-api      - Run API tests"
	@echo "  test-frontend - Run frontend tests"
	@echo "  lint          - Run all linters"
	@echo "  lint-api      - Run API linters"
	@echo "  lint-frontend - Run frontend linters"
	@echo "  clean         - Clean all build and temporary files"
	@echo "  dev-api       - Run API development server"
	@echo "  dev-frontend  - Run frontend development server"
