# Customer Churn Prediction (MLOps Pipeline)

[![Project Repository](https://img.shields.io/badge/Project-Repository-blue?style=flat-square&logo=github)](https://github.com/Alihmidov/customer-churn-mlops-pipeline)
[![Github Profile](https://img.shields.io/badge/Github-Profile-black?style=flat-square&logo=github)](https://github.com/Alihmidov)

This repository contains an end-to-end Machine Learning pipeline to predict customer churn. The model is built using CatBoost, served via FastAPI, containerized with Docker, tracked via MLflow, and versioned with DVC using modern dependency management via uv.

## Live API Endpoints
The service is deployed on Render and accepts requests at these links:
* **Production Base URL:** [https://customer-churn-api-pz8n.onrender.com](https://customer-churn-api-pz8n.onrender.com)
* **Interactive API Docs (Swagger UI):** [https://customer-churn-api-pz8n.onrender.com/docs](https://customer-churn-api-pz8n.onrender.com/docs)

---

## 💡 Architectural Decisions

### Why CatBoost?
* **Categorical features:** CatBoost handles categorical splits natively during training, removing the need for heavy manual preprocessing (like One-Hot Encoding) and drastically reducing data leakage risks.
* **Overfitting resistance:** Built-in ordered boosting mechanisms prevent target leakage, allowing the model to generalize perfectly on our ~440k dataset without requiring extreme hyperparameter tuning.
* **Deployment speed:** Models serialize cleanly into lightweight `.cbm` binary files, resulting in sub-millisecond inference latencies inside the production API layer.

### Why FastAPI instead of Flask/Django?
* **Async performance:** Built natively on Starlette and Uvicorn, FastAPI easily handles concurrent prediction payloads without blocking asynchronous execution threads.
* **Pydantic validation:** Inputs are strictly type-checked at the gateway layer using Pydantic validation schemas. Malformed or invalid JSON structures are automatically blocked with HTTP 422 errors before reaching the machine learning estimator.
* **Auto documentation:** Interactive Swagger UI documentation is generated automatically, simplifying remote endpoint validation and client integration testing.

---

## 📊 Model Performance & Data Validation

### 1. Training Metrics
The CatBoost model yields the following classification capabilities over the heavy validation subset (88,167 samples):

* **Accuracy:** 98.72%
* **ROC AUC Score:** 0.9888

**Classification Report:**
```text
              precision    recall  f1-score   support

           0       0.97      1.00      0.99     38044
           1       1.00      0.98      0.99     50123

    accuracy                           0.99     88167
   macro avg       0.99       0.99      0.99     88167
weighted avg       0.99       0.99      0.99     88167

Confusion Matrix:
Plaintext

[[38044     0]
 [ 1124 48999]]

2. Production API Live Test (Swagger UI)

Below are execution instances confirming that the live cloud API successfully validates raw JSON schema bodies and generates low-latency responses:

Project Architecture & Pipeline Logic
1. SQL & Data Ingestion Layer

    Database Constraints: Native relational queries were executed within sql/analysis.sql to isolate raw input parameters and verify baseline data integrity.

    Secure Pipeline Extraction: Configured data_ingestion.py scripts to dynamically connect to the live PostgreSQL backend instance and pipe raw training data directly into python computing blocks.

2. Exploratory Data Analysis (EDA)

Data quality checks and class constraints were verified comprehensively within Jupyter notebooks before building core production transforms:

    Target Balance: Validated binary label status using target metrics (revealing a predictable 56.7% vs 43.3% structural ratio).

    Feature Distributions: Audited raw numeric features simultaneously using isolated df.hist() commands to track skewness.

    Scale Variance Boxplots: Developed automated for loop scripts iterating over isolated horizontal sns.boxplot frameworks to evaluate individual attribute scales without compression artifacts.

3. Pipeline Feature Engineering

Constructed strict operational data transformations within data_transformation.py to map customer risk behaviors:

    Age Group Segmentation: Maps raw customer ages into logical lifecycle groupings.

    Passive User Flags: Computes discrete engagement benchmarks based on overall usage frequencies.

    Critical Payment Risk Indicator: Explicitly flags customers triggering severe transaction delays (Payment Delay > 20).

4. Containerization & Modern MLOps Tooling

    Package Management via uv: Replaced slow pip/poetry wrappers with Astral's uv tool for blazing-fast package resolution and strictly deterministic synchronization using locked environments (uv.lock).

    Data Versioning (DVC): Integrated DVC to isolate heavy raw CSV data elements into localized decoupling directories (C:\dvc_storage), keeping tracking points transparent and Git tracking clean.

    Experiment Management: Standard logs and validation passes are stored within notebooks/ tracking trees to verify optimization changes.

Repository Structure
Plaintext

customer-churn-mlops-pipeline/
├── .github/workflows/
│   └── main.yml                  # GitHub Actions CI/CD pipeline configuration
├── app/                          # Production FastAPI Web Application
│   ├── main.py                   # Application entry point
│   ├── routes/
│   │   └── api.py                # Core POST prediction routing map
│   └── schemas/
│       └── request_body.py       # Pydantic data validation model structures
├── assets/                       # Documentation assets and screenshots
├── config/
│   ├── hyperparams.yaml          # Static model hyperparameter configurations
│   └── settings.py               # Database and configuration setup bindings
├── models/                       # Serialized CatBoost model files (.cbm)
├── notebooks/                    # Experimental EDA loops, boxplots, and training iterations
├── pipelines/                    # Operational automation extraction and feature generation
│   ├── 01_ingestion.py
│   ├── 02_feature_engineering.py
│   └── 03_evaluation.py
├── sql/                          # Native PostgreSQL analytical scripts and schemas
│   ├── queries.sql
│   └── schema.sql
├── tests/                        # Automated Pytest suite validations
│   ├── conftest.py
│   ├── test_feature_engineering.py
│   ├── test_predict.py
│   └── test_preprocessing.py
├── utils/                        # System loggers and modular wrapper utilities
│   ├── helpers.py
│   └── logging_config.py
├── .dockerignore
├── .dvcignore
├── .env.example
├── Dockerfile                    # Highly optimized application runtime image container
├── Dockerfile.mlflow             # Isolated tracking image structure
├── docker-compose.yml            # Multi-service deployment orchestration stack
├── pyproject.toml / uv.lock     # Secure Python package locks managed by uv
└── README.md

Local Setup & Replication

Ensure you have Python 3.12 and uv installed globally.
1. Environment Synchronization

Clone the project, build a mirrored virtual environment, and sync locked dependencies:
Bash

uv sync --frozen

2. Run Data Transformation

Execute the full database feature engineering and matrix manipulation workflows:
Bash

uv run python pipelines/data_transformation.py

3. Start Local FastAPI Instance

Boot up the development web application container locally with reload settings:
Bash

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Test the functional local endpoints and schemas using the automated interface at: http://localhost:8000/docs
Docker Deployment
Standalone API Server

To manually compile and deploy the primary inference app container locally on port 8000:
Bash

# Build the core container
docker build -t customer-churn-api .

# Run the inference container layer
docker run -p 8000:8000 customer-churn-api

Multi-Service Infrastructure (FastAPI + MLflow Stack)

To orchestrate the full decoupled model environment with compose architecture simultaneously:
Bash

docker-compose up --build

Testing Guardrails

Execute the complete validation block via pytest locally to confirm API behavior, integration checks, and logic constraints:
Bash

uv run pytest tests/