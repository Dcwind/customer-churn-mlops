# Development Workflow
train:
	pipenv run python src/train.py

mlflow-ui:
	pipenv run mlflow ui

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
all: install lint format test
