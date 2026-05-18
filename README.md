# Customer Churn Prediction (MLOps Pipeline)

[![Project Repository](https://img.shields.io/badge/Project-Repository-blue?style=flat-square&logo=github)](https://github.com/Alihmidov/customer-churn-mlops-pipeline)
[![Github Profile](https://img.shields.io/badge/Github-Profile-black?style=flat-square&logo=github)](https://github.com/Alihmidov)

This repository contains an end-to-end Machine Learning pipeline designed to predict customer churn. The core modeling engine is powered by **CatBoost**, served via an asynchronous **FastAPI** web service, containerized with **Docker**, and managed deterministically using **uv**.

Live API Endpoints
The service is fully deployed and actively serving inference requests:

Production Base URL: https://customer-churn-api-pz8n.onrender.com
Interactive API Docs (Swagger UI): https://customer-churn-api-pz8n.onrender.com/docs


Model Performance & Proof of Concept
1. Training Metrics
The CatBoost model demonstrates high robustness on evaluation splits:

Accuracy: 98.72%
ROC AUC Score: 0.9888

Classification Report:
text              precision    recall  f1-score   support

           0       0.97      1.00      0.99     38044
           1       1.00      0.98      0.99     50123

    accuracy                           0.99     88167
   macro avg       0.99      0.99      0.99     88167
weighted avg       0.99      0.99      0.99     88167

Confusion Matrix:
[[38044     0]
 [ 1124 48999]]

2. Production API Live Test (Swagger UI)
Below is the execution instance verifying that the live cloud API successfully parses incoming JSON payloads and yields fast, correct predictions:
![Swagger UI Request](https://github.com/Alihmidov/customer-churn-mlops-pipeline/blob/main/assets/swagger_ui_request.png?raw=true)
![Swagger UI Response](https://github.com/Alihmidov/customer-churn-mlops-pipeline/blob/main/assets/swagger_ui_response.png?raw=true)

Project Architecture & Workflow

SQL Pre-modeling Layer: Initial exploratory data analysis and database-level constraints were engineered directly inside sql/analysis.sql on the raw PostgreSQL data layer.
Experimental Layer: Feature targeting rules and structural handling were prototyped systematically within local .ipynb files.
Production Pipelines: Operational steps are structured into clean Python scripts:

data_ingestion.py: Connects securely and extracts historical inputs from the database layer.
data_transformation.py: Formulates automated feature mapping including customer age constraints, passive user flags, and risk indicators like critical payment lags (Payment Delay > 20).


Containerized Deployment: FastAPI safely loads the trained model weights into memory during application startup and handles requests via an optimized Docker container setup.


Repository Structure
textcustomer-churn-mlops-pipeline/
├── .github/workflows/main.yml  # GitHub Actions automated test suite
├── app/                        # FastAPI Web Application
│   ├── inference/predict.py    # Path-resilient model loader and class wrapper
│   ├── routes/api.py           # Core POST endpoint route mapping
│   └── schemas/request_body.py # Pydantic strict payload model definitions
├── assets/                     # Visual deployment proof artifacts
├── models/                     # Serialized CatBoost model binary (.cbm)
├── notebooks/                  # Sequential EDA and training iterations
├── pipelines/                  # Live execution data pipelines
├── sql/                        # Multi-stage preprocessing database scripts
├── tests/                      # Pytest automated testing routines
├── Dockerfile                  # Container build instructions
├── pyproject.toml / uv.lock    # Deterministic environment definitions
└── README.md

Local Environment Setup
Ensure Python 3.12 and the uv tool are configured locally.
1. Synchronize Virtual Environment
bashuv sync --frozen
2. Run Feature Transformation
bashuv run python pipelines/data_transformation.py
3. Start Local FastAPI Instance
bashuv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Test interactively at http://localhost:8000/docs.

Docker Deployment
bash# Build the application image
docker build -t customer-churn-api .

# Run the inference layer standalone
docker run -p 8000:8000 customer-churn-api
For orchestration containing tracking integrations (FastAPI + MLflow):
bashdocker-compose up --build

Testing Guardrails
To validate system health and catch potential inference schema breaks:
bashuv run pytest tests/