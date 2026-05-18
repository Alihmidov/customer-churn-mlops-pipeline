# Customer Churn Prediction (MLOps Pipeline)

[![Project Repository](https://img.shields.io/badge/Project-Repository-blue?style=flat-square&logo=github)](https://github.com/Alihmidov/customer-churn-mlops-pipeline)
[![Github Profile](https://img.shields.io/badge/Github-Profile-black?style=flat-square&logo=github)](https://github.com/Alihmidov)

This repository contains an end-to-end Machine Learning pipeline designed to predict customer churn. The core modeling engine is powered by **CatBoost**, served via an asynchronous **FastAPI** web service, containerized with **Docker**, and managed deterministically using **uv**.

## 🚀 Live API Endpoints
The service is fully deployed and actively serving inference requests:
* **Production Base URL:** [https://customer-churn-api-pz8n.onrender.com](https://customer-churn-api-pz8n.onrender.com)
* **Interactive API Docs (Swagger UI):** [https://customer-churn-api-pz8n.onrender.com/docs](https://customer-churn-api-pz8n.onrender.com/docs)

---

## 📊 Model Performance & Proof of Concept

### 1. Training Metrics
The CatBoost model demonstrates high robustness on evaluation splits with minimal false positives:
* **Accuracy:** 98.72%
* **ROC AUC Score:** 0.9888

**Classification Report:**
```text
              precision    recall  f1-score   support

           0       0.97      1.00      0.99     38044
           1       1.00      0.98      0.99     50123

    accuracy                           0.99     88167
   macro avg       0.99      0.99      0.99     88167
weighted avg       0.99      0.99      0.99     88167

Confusion Matrix:
Plaintext

[[38044     0]
 [ 1124 48999]]

2. Live Deployment Proof

The service logs confirm smooth initialization, package synchronization via uv, and successful loading of the binary serialized weights into memory within the Render production container:
3. Production API Live Test (Swagger UI)

Below is an execution instance showing a fast response check from the production gateway endpoint (/api/v1/predict) utilizing direct customer telemetry fields:
🏗️ Project Architecture & Workflow

    SQL Pre-modeling Layer: Initial exploratory analysis and database-level constraints were engineered directly inside sql/analysis.sql on the raw PostgreSQL data layer.

    Experimental Layer: Feature targeting rules and structural handling were prototyped systematically within local .ipynb files.

    Production Pipelines: Operational steps are structured into clean Python scripts:

        data_ingestion.py: Connects securely and extracts historical inputs from the database layer.

        data_transformation.py: Formulates automated feature mapping including customer age constraints, passive user flags, and risk indicators like critical payment lags (Payment Delay > 20).

    Containerized Deployment: FastAPI directly initialises the model configuration safely inside a yml-configured environment. System operations use a unified Dockerfile utilizing uv for caching.

📁 Repository Structure
Plaintext

customer-churn-mlops-pipeline/
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

🛠️ Local Environment Setup

Ensure Python 3.12 and the uv tool are configured locally.
1. Synchronize Virtual Environment
Bash

uv sync --frozen

2. Run Feature Transformation
Bash

uv run python pipelines/data_transformation.py

3. Start Local FastAPI Instance
Bash

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Test interactively at http://localhost:8000/docs.
🐳 Docker Deployment

The application logic can be local-built or stacked instantly using container tools:
Bash

# Build the application image
docker build -t customer-churn-api .

# Run the inference layer standalone
docker run -p 8000:8000 customer-churn-api

For orchestration containing tracking integrations (FastAPI + MLflow):
Bash

docker-compose up --build