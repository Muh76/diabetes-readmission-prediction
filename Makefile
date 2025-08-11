.PHONY: help install setup test lint format clean build run-api run-streamlit deploy

help: ## Show this help message
	@echo "Diabetes Readmission Prediction - Available Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
	pip install -e ".[dev]"

setup: ## Setup pre-commit hooks and development environment
	pre-commit install
	pre-commit install --hook-type commit-msg

test: ## Run tests with coverage
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	ruff check src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format: ## Format code with black and isort
	black src/ tests/
	isort src/ tests/
	ruff check --fix src/ tests/

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/ .pytest_cache/ .coverage

build: ## Build Docker image
	docker build -t diabetes-readmission:latest .

run-api: ## Run FastAPI locally
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

run-streamlit: ## Run Streamlit locally
	streamlit run src/app/streamlit/main.py

deploy: ## Deploy to Azure Container Apps
	az containerapp update \
		--name diabetes-readmission \
		--resource-group your-resource-group \
		--image your-acr-name.azurecr.io/diabetes-readmission:latest

mlflow-ui: ## Start MLflow tracking server
	mlflow ui --host 0.0.0.0 --port 5000

notebook: ## Start Jupyter notebook
	jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

data-exploration: ## Run initial data exploration
	python -m src.data.explore_data

train-model: ## Train baseline model
	python -m src.models.train_baseline

evaluate-model: ## Evaluate trained model
	python -m src.models.evaluate_model
