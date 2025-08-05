# Customer Churn Prediction: MLOps Capstone

---

## Introduction

This repository contains the implementation of an end-to-end MLOps pipeline for predicting customer churn in a telecom company. The project demonstrates core MLOps principles, including experiment tracking, orchestration, model deployment, monitoring, and best practices for reproducibility and scalability. It serves as the final capstone for the MLOps course, showcasing a cloud-ready, extensible, and reproducible machine learning service.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
- [Data](#data)
- [Experiment Tracking](#experiment-tracking)
- [Orchestration](#orchestration)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Best Practices](#best-practices)
- [Setup](#setup)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Future Works](#future-works)
- [Acknowledgements](#acknowledgements)

---

## Problem Statement

Telecom providers face significant revenue loss due to customer churn. By predicting which customers are likely to leave one month in advance, companies can offer targeted retention incentives to reduce churn. This project builds a binary classifier to flag high-risk customers, enabling proactive retention strategies.

---

## System Architecture
![System Architecture](./assets/mlops-system-architecture.svg)

---

## Data

The dataset is sourced from the IBM Telco Customer Churn dataset, publicly available as a CSV file.

- **Source**: IBM Telco Customer Churn CSV
- **Size**: ~1 MB, ~7043 rows, 21 features
- **Target Variable**: Churn (Outcome: Yes/No)
- **Features**: Customer demographics, account information, and service usage details

The dataset is small, facilitating fast iteration during development.

---

## Experiment Tracking

Experiment tracking is managed using **MLflow** with a local server backed by S3 for artifact storage. All model training runs, hyperparameters, and metrics are logged to MLflow. The best-performing model is registered in the MLflow model registry as the "Production" model for deployment.

- **Tool**: MLflow
- **Metrics Tracked**: PR-AUC (primary), Accuracy, F1 (secondary)
- **Artifacts**: Trained models, preprocessing pipelines

---

## Orchestration

Workflow orchestration is handled by **Prefect 2**, which manages the training pipeline. Prefect flows are Python-native, with built-in retries and scheduling capabilities.

- **Pipelines**:
  - `mvp_training_flow`: Runs the `src/train.py` script as a subprocess within the project's virtual environment using `pipenv`.
- **Tool**: Prefect 2
- **Storage**: AWS S3 for input data and logs

---

## Deployment

The model is deployed as a **FastAPI** inference service, containerized using **Docker** for portability. The service loads the Production model from the MLflow registry and exposes an API endpoint for real-time predictions.

- **Tools**: FastAPI, Uvicorn, Docker
- **Model**: Scikit-learn pipeline (preprocessing + LogisticRegression)
- **Artifact Source**: MLflow model registry
- **Deployment**: Local or cloud-ready (e.g., ECS Fargate as a stretch goal)

---

## Monitoring

(This feature is not yet functional.) Model and data monitoring are to be implemented using **Evidently**, which generates HTML reports and JSON flags for drift and performance issues. If drift is detected, a retrain flow would be triggered via Prefect.

- **Tool**: Evidently
- **Metrics Monitored**: Data drift, model performance (PR-AUC, Accuracy, F1)
- **Output**: HTML report, JSON flag for retraining
- **Alerting**: Slack alerts as a stretch goal

---

## Best Practices

The project adheres to MLOps best practices to ensure reproducibility, maintainability, and quality:

- **Unit Tests**: Pytest for testing data preprocessing, model training, and API endpoints.
- **Integration Tests**: REST API-based prediction endpoint testing by testing adding sample customer
- **Linting & Formatting**: Pre-commit hooks with isort, black, and pylint.
- **CI/CD**: GitHub Actions for linting, testing, and Docker image builds.
- **Automation**: Makefile for managing dependencies, builds, and runs.
- **Reproducibility**: Pinned dependencies in `requirements.txt`, clear README with setup instructions.

---

## Setup

### Prerequisites

- Python 3.12
- `pipenv`
- Docker and Docker Compose
- A Unix-based system (MacOS/Linux)
– Terraform v1.12.2+
- AWS CLI (for Terraform and S3 configuration)
– An AWS account and an administrative IAM user

### 🚀 Setup Instructions

Follow these steps to set up the project environment and run the MLOps pipeline on your local machine.

#### 1. Initial Setup (One-Time Action)

Follow these steps the first time you clone the repository.

**1.1. Clone the Repository**

```bash
git clone https://github.com/Dcwind/customer-churn-mlops.git
cd customer-churn-mlops
```

**1.2. Create and Activate a Virtual Environment**

It is crucial to work inside a virtual environment to manage project dependencies and avoid conflicts with your global Python installation. You have two options:

**Option A: Using pipenv (Recommended)**

This is the simplest method as it handles environment creation and package installation in one step.

```bash
# This command creates a virtual environment and installs all dependencies
pipenv install --dev

# Activate the virtual environment shell
pipenv shell
```

**Option B: Using venv (Standard Python)**

If you prefer not to use pipenv, you can use Python's built-in venv module.

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install all necessary dependencies for development
make install
```

*Note*: All subsequent commands in this setup guide should be run from within the activated virtual environment.

**1.3. Set Up Pre-commit Hooks**

This project uses pre-commit to automatically run code quality checks before each commit. This only needs to be set up once per project clone.

```bash
# Install the git hooks
pre-commit install
pre-commit autoupdate
```

**1.4. Configure AWS Admin Credentials**

Configure the AWS CLI with your main administrative IAM user credentials. This is required to run Terraform.

```bash
aws configure
```

Verify your identity with:

```bash
aws sts get-caller-identity
```

**1.5. Provision Cloud Infrastructure**

Navigate to the terraform directory and run the following commands to create the S3 bucket and a dedicated, low-privilege IAM user for the application.

```bash
cd terraform
terraform init
terraform apply
```

When prompted, type `yes` to approve. After the command completes, use `terraform output` to get the access keys for the newly created `mlflow-s3-user`.

**1.6. Configure Application AWS Profile**

Configure a new AWS CLI profile for the application using the credentials you just generated from Terraform.

```bash
# Go back to the project root
cd ..

# Configure the new profile
aws configure --profile mlflow-app
```

**1.7. Initialize Project Directories**

This command creates the necessary mlruns directory with the correct user permissions.

```bash
make init
```

#### 2. Development Workflow

This is the standard day-to-day workflow for running the application. You will need at least two separate terminals, both running inside the activated pipenv shell.

**2.1. Start the MLflow Server (Terminal 1)**

In your first terminal, start the MLflow server. It will now use your S3 bucket for artifact storage.

```bash
make mlflow-ui
```

You can now access the MLflow dashboard in your browser at `http://localhost:5000`.

**2.2. Run an Initial Training Job (Terminal 2)**

Before starting the prediction service, you must train and register at least one model. With the MLflow server running, execute the training script.

```bash
make train
```

Alternatively, to run the orchestrated training pipeline:

```bash
make orchestrate
```

**2.3. Run the Prediction Service (Terminal 2 or 3)**

Once a model has been registered, you can build and run the containerized prediction service.

```bash
# Build the Docker image
make docker-build

# Run the container
make docker-run
```

You can now access the prediction service's health check at `http://localhost:8000/health` and its interactive API documentation at `http://localhost:8000/docs`.

**2.4. Run Subsequent Training Jobs (Optional)**

You can now run `make train` or `make orchestrate` at any time to register new model versions. The prediction service will automatically load the latest version the next time it restarts.

#### 3. Stopping the Application

To stop the services, press `Ctrl+C` in the respective terminals.

---

## 🧪 Running Tests

This project includes a suite of tests to ensure code quality and correctness. The tests are written using `pytest`.

### Test Types

* **Unit Tests**: Located in `tests/`, these tests check small, isolated pieces of code, such as individual functions. They are fast and do not require any external services to be running.
* **Integration Tests**: Also in `tests/`, these tests verify that different components of the system work together correctly. For this project, the integration test checks the live, containerized prediction service.

### How to Run the Tests

All tests can be run using a single command from the `Makefile`. Make sure you are inside the activated `pipenv shell` before running the commands.

#### Running All Tests

To run the entire test suite (both unit and integration tests), you must have the application services running first.

**Step 1: Start the Services (in separate terminals)**

```bash
# In Terminal 1
make mlflow-ui

# In Terminal 2
make serve-docker
```

**Step 2: Run the Test Suite (in Terminal 3)**

```bash
make test
```

`pytest` will automatically discover and run all test files in the `tests/` directory.

#### Running Only Unit Tests

If you want to quickly run only the unit tests without starting the full application stack, you can run pytest and tell it to ignore the integration test file.

```bash
# This command runs all tests EXCEPT the integration test
pipenv run python -m pytest --ignore=tests/test_prediction_service.py
```

---

## Project Structure

```
customer-churn-mlops/
│
├── src/                       # Source code modules
|   ├── data_processing.py     # Data loader and preprocessor
│   └── train.py               # Model training pipeline in MLFlow
│
├── orchestration/             # Workflow orchestration
|   ├── generate_report.py     # Generate a data-drift report using Evidently
│   └── flows.py               # Automated training pipeline using Prefect
│
├── deployment/                # Model deployment
|   ├── Dockerfile             # Setup dependencies, starts Uvicorn server
│   └── app.py                 # API endpoints
│
├── terraform/                 # Terraform configurations
|   ├── main.tf                # AWS S3 and IAM configuration
|   └── variables.tf           # AWS variables
|
├── tests/                           # Test suite
|   ├── test_data_processing.py      # Data processor testing
│   └── test_prediction_service.py   # Prediction service testing
│
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Python dependencies for dev mode
├── pyproject.toml             # Project configuration
├── Makefile                   # Automation commands
├── docker-compose.yml         # Multi-container orchestration
├── .pre-commit-config.yaml    # Code quality hooks
├── .github/                   # GitHub Actions workflows
│   └── workflows/
├── Pipfile                    # Pip package description
└── README.md                  # Project documentation
```

---

## Sample Run

Below are screenshots showcasing key components of the MLOps pipeline for the Customer Churn Prediction project.

### Pre-commit Runs
![Pre-commit Run](./screenshots/precommit-3.png)
![Pre-commit Run](./screenshots/precommit-4.png)

### First Run
First run by calling `train.py`:
![First Run](./screenshots/firstrun-1.png)

**Metric Snapshot:**
| Metric   | Value  | Interpretation                                                                 |
|----------|--------|-------------------------------------------------------------------------------|
| PR-AUC   | 0.6365 | Very strong, you're catching churners well while keeping false positives low. |
| Accuracy | 0.7977 | Good, but not very informative on imbalanced data (most customers don’t churn). |
| F1 Score | 0.5568 | Solid balance between precision and recall. Shows your model isn't just guessing. |

When running `make orchestrate`, it also runs a training:
- ![Orchestration](./screenshots/orchestration-7.png)

### MLflow UI
Results of the first try are shown in the MLFlow UI:
![MLflow UI](./screenshots/mlflow-2.png)

After a few more runs, the training results are shown as such:
![Multiple Runs](./screenshots/multipleruns-5.png)

## Miscellaneous Screenshots

### FastAPI Documentation
![FastAPI Documentation](./screenshots/fastapi-6.png)

### AWS Access
- ![AWS Access](./screenshots/aws-8.png)

### Evidently Project List
- ![Evidently Project List](./screenshots/evidently-9.png)

### Pytest Run
- ![Pytest Run](./screenshots/pytest-10.png)

### Github Actions
- ![Github Actions Running](./screenshots/git-11.png)
- ![Github Actions Ran](./screenshots/git-12.png)

---

## Future Works

- Developing a functional monitoring component as described.
- Deploy the FastAPI service to ECS Fargate for scalability.
- Set up Slack alerts for drift detection.
