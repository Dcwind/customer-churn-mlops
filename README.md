# Customer Churn Prediction: MLOps Capstone

---

## Introduction

This repository contains the implementation of an end-to-end MLOps pipeline for predicting customer churn in a telecom company. The project demonstrates core MLOps principles, including experiment tracking, orchestration, model deployment, monitoring, and best practices for reproducibility and scalability. It serves as the final capstone for the MLOps course, showcasing a cloud-ready, extensible, and reproducible machine learning service.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Data](#data)
- [Experiment Tracking](#experiment-tracking)
- [Orchestration](#orchestration)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Best Practices](#best-practices)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Future Works](#future-works)
- [Acknowledgements](#acknowledgements)

---

## Problem Statement

Telecom providers face significant revenue loss due to customer churn. By predicting which customers are likely to leave one month in advance, companies can offer targeted retention incentives to reduce churn. This project builds a binary classifier to flag high-risk customers, enabling proactive retention strategies.

---

## Data

The dataset is sourced from the IBM Telco Customer Churn dataset, publicly available as a CSV file.

- **Source**: IBM Telco Customer Churn CSV
- **Size**: ~1 MB, ~7043 rows, 21 features
- **Target Variable**: Churn (Outcome: Yes/No)
- **Features**: Customer demographics, account information, and service usage details

The dataset is small, enabling fast iteration during development, while still being rich enough to support a complete demonstration of the MLOps workflow.

---

## Experiment Tracking

Experiment tracking is managed using **MLflow** with a local server backed by S3 for artifact storage. All model training runs, hyperparameters, and metrics are logged to MLflow. The best-performing model is registered in the MLflow model registry as the "Production" model for deployment.

- **Tool**: MLflow
- **Metrics Tracked**: PR-AUC (primary), Accuracy, F1 (secondary)
- **Artifacts**: Trained models, preprocessing pipelines
- **Notebook**: [Placeholder for experiment notebook, e.g., `notebooks/experiments.ipynb`]

