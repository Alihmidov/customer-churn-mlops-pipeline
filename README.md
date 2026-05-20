Customer Churn Prediction (MLOps Pipeline)

This repository contains an end-to-end Machine Learning pipeline to predict customer churn. The model is built using CatBoost, served via FastAPI, containerized with Docker, and managed using uv.
Live API Endpoints

The service is deployed on Render and accepts requests at these links:

    Production Base URL: https://customer-churn-api-pz8n.onrender.com
    Interactive API Docs (Swagger UI): https://customer-churn-api-pz8n.onrender.com/docs

Architectural Decisions
Why CatBoost?

    Categorical features: CatBoost handles categorical splits natively during training, removing the need for One-Hot Encoding and reducing data leakage risks.
    Overfitting resistance: Built-in ordered boosting prevents target leakage, allowing the model to generalize well on the ~440k dataset without heavy hyperparameter tuning.
    Deployment speed: Models serialize into lightweight .cbm binary files, resulting in fast inference inside the production API.

Why FastAPI instead of Flask/Django?

    Async performance: Built on Starlette and Uvicorn, FastAPI handles concurrent prediction requests without blocking.
    Pydantic validation: Inputs are type-checked at the gateway layer. Invalid payloads are blocked with HTTP 422 errors before reaching inference logic.
    Auto documentation: Swagger UI is generated automatically, simplifying testing and integration.

Model Performance
Training Metrics

    Accuracy: 98.72%
    ROC AUC Score: 0.9888

Classification Report:

              precision    recall  f1-score   support

           0       0.97      1.00      0.99     38044
           1       1.00      0.98      0.99     50123

    accuracy                           0.99     88167
   macro avg       0.99      0.99      0.99     88167
weighted avg       0.99      0.99      0.99     88167

Confusion Matrix:
[[38044     0]
 [ 1124 48999]]

Production API Live Test (Swagger UI)

Swagger UI Request Swagger UI Response
Project Architecture

1. SQL & Data Ingestion Layer

    Wrote PostgreSQL queries inside sql/analysis.sql to analyze raw data and verify constraints.
    Built data_ingestion.py to connect to the live PostgreSQL instance and extract the dataset.

2. Exploratory Data Analysis

    Evaluated class balance and feature distributions inside Jupyter notebooks.
    Used boxplots for outlier detection across all numerical columns.

3. Feature Engineering

    Created binary risk flags in data_transformation.py:
        Age group segmentation
        Passive user flags based on engagement
        Critical payment delay indicator (Payment Delay > 20)

4. Containerization & Deployment

    Replaced pip with uv for fast, deterministic dependency management.
    Deployed FastAPI via Docker container on Render.

Repository Structure

customer-churn-mlops-pipeline/
├── .github/workflows/main.yml   # GitHub Actions CI/CD
├── app/
│   ├── inference/predict.py     # Model loader and inference logic
│   ├── routes/api.py            # POST endpoint
│   └── schemas/request_body.py  # Pydantic validation
├── assets/                      # Screenshots
├── models/                      # CatBoost model file (.cbm)
├── notebooks/                   # EDA and training notebooks
├── pipelines/                   # Data ingestion and transformation
├── sql/                         # PostgreSQL analysis scripts
├── tests/                       # Pytest test suite
├── Dockerfile
├── pyproject.toml / uv.lock
└── README.md

Local Setup

Python 3.12 and uv required.

# Install dependencies
uv sync --frozen

# Run data transformation
uv run python pipelines/data_transformation.py

# Start local API
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Test at http://localhost:8000/docs.
Docker

docker build -t customer-churn-api .
docker run -p 8000:8000 customer-churn-api

For FastAPI + MLflow together:

docker-compose up --build

Tests

uv run pytest tests/

