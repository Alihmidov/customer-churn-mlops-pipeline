# Customer Churn Prediction (MLOps Pipeline)

[![Project Repository](https://img.shields.io/badge/Project-Repository-blue?style=flat-square&logo=github)](https://github.com/Alihmidov/customer-churn-mlops-pipeline)
[![Github Profile](https://img.shields.io/badge/Github-Profile-black?style=flat-square&logo=github)](https://github.com/Alihmidov)

This repository contains an end-to-end Machine Learning pipeline to predict customer churn. The model is built using CatBoost, served via FastAPI, containerized with Docker, and managed using uv.

## Live API Endpoints
The service is deployed on Render and accepts requests at these links:
* **Production Base URL:** https://customer-churn-api-pz8n.onrender.com
* **Interactive API Docs (Swagger UI):** https://customer-churn-api-pz8n.onrender.com/docs

---

## Model Performance & Proof of Concept

### 1. Training Metrics
The CatBoost model shows the following evaluation metrics:
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

2. Production API Live Test (Swagger UI)

Below is the execution instance verifying that the live cloud API successfully parses incoming JSON payloads and yields fast, correct predictions:
Project Architecture & Workflow

    SQL Pre-modeling Layer: Initial data analysis and database constraints were handled inside sql/analysis.sql on the PostgreSQL data layer.

    Experimental Layer: Data cleaning, EDA, and features were prototyped inside Jupyter notebooks (.ipynb).

    Production Pipelines: Operational steps are automated using Python scripts:

        data_ingestion.py: Connects to PostgreSQL and extracts data.

        data_transformation.py: Formulates feature mapping including age groups, passive user flags, and risk indicators like payment lags (Payment Delay > 20).

    Containerized Deployment: FastAPI loads the trained model weights into memory when the application starts and serves requests inside a Docker container.

Repository Structure
Plaintext

customer-churn-mlops-pipeline/
├── .github/workflows/main.yml  # GitHub Actions automated test suite
├── app/                        # FastAPI Web Application
│   ├── inference/predict.py    # Model loader and class wrapper
│   ├── routes/api.py           # Core POST endpoint route mapping
│   └── schemas/request_body.py # Pydantic data validation models
├── assets/                     # Screenshots for documentation
├── models/                     # Serialized CatBoost model file (.cbm)
├── notebooks/                  # Experimental EDA and training iterations
├── pipelines/                  # Data ingestion and transformation pipelines
├── sql/                        # SQL scripts for database analysis
├── tests/                      # Pytest test cases
├── Dockerfile                  # Production Docker configuration
├── pyproject.toml / uv.lock    # Python dependencies managed by uv
└── README.md

Local Environment Setup

Make sure Python 3.12 and the uv tool are installed on your machine.
1. Synchronize Virtual Environment
Bash

uv sync --frozen

2. Run Feature Transformation
Bash

uv run python pipelines/data_transformation.py

3. Start Local FastAPI Instance
Bash

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

You can test the local API at http://localhost:8000/docs.
Docker Deployment

You can build and run the application standalone using Docker:
Bash

# Build the application image
docker build -t customer-churn-api .

# Run the inference layer standalone
docker run -p 8000:8000 customer-churn-api

To run both FastAPI and MLflow services together:
Bash

docker-compose up --build

Testing Guardrails

Run the test suite with pytest to check code health and API schemas:
Bash

uv run pytest tests/