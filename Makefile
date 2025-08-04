# Main Project Workflow
# One-time setup to create necessary directories with correct permissions.
init:
	mkdir -p mlruns/artifacts

# Development Workflow
train:
	pipenv run python src/train.py

mlflow-ui:
	pipenv run mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db \
	--default-artifact-root ./mlruns/artifacts


serve:
	pipenv run uvicorn deployment.app:app --reload

orchestrate:
	pipenv run python orchestration/flows.py

# Docker Workflow
docker-build:
	docker build -f deployment/Dockerfile -t churn-prediction-service .

docker-run:
	docker run \
  		--network="host" \
 		-v "$$(pwd)/mlruns:/workspaces/customer-churn-mlops/mlruns" \
		-p 8000:8000 \
  		churn-prediction-service

# Docker Compose Workflow
compose-up:
	docker-compose up --build

compose-down:
	docker-compose down

# Installation
# Install ALL dependencies for a DEVELOPMENT environment
install:
	pip install --upgrade pip &&\
		pip install -r requirements-dev.txt

# Install ONLY production dependencies (for Docker, CI/CD)
install-prod:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# Code Quality
# Run code quality tools within the pipenv environment.
lint:
	pipenv run flake8 src/

format:
	pipenv run black src/

# Testing
test:
	pipenv run pytest

# Run all tasks
# all: install lint format test
