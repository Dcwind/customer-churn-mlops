# Main Project Workflow
# One-time setup to create necessary directories with correct permissions.
init:
	mkdir -p mlruns/artifacts

# Dependency Management
# Run this command after adding/removing packages with pipenv to update
# the requirements.txt files.
requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

# Development Workflow
train:
	pipenv run python src/train.py

mlflow-ui:
	export AWS_PROFILE=mlflow-app && \
	pipenv run mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db \
	--default-artifact-root s3://churn-mlops-artifacts-arriving-crow/


serve:
	pipenv run uvicorn deployment.app:app --reload

orchestrate:
	pipenv run python orchestration/flows.py

# Generate a visual data drift report using Evidently.
report:
	pipenv run python orchestration/generate_report.py

# Docker Workflow
docker-build:
	docker build -f deployment/Dockerfile -t churn-prediction-service .

docker-run:
	docker run --rm -it \
	  -e AWS_PROFILE=mlflow-app \
	  --network="host" \
	  -v "$$(pwd)/mlruns:/workspaces/customer-churn-mlops/mlruns" \
	  -v ~/.aws:/root/.aws \
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
