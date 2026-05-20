# Customer Churn Prediction (MLOps Pipeline)

This repository contains an end-to-end Machine Learning pipeline to predict customer churn. The project emphasizes production-ready practices, including containerized deployment, remote model management, and CI/CD automation.

## Live API Endpoints

The service is deployed on Render and is ready for inference:

- [Production Base URL](https://customer-churn-api-pz8n.onrender.com)
- [Interactive API Docs (Swagger UI)](https://customer-churn-api-pz8n.onrender.com/docs)

> **Note:** Free tier — first request may take ~60s to wake up.

## Architectural Decisions

### Model Management Strategy

To ensure a clean repository and follow production best practices, the model is not stored in Git. Instead, it is hosted on Hugging Face Hub and fetched dynamically during the API startup using `huggingface_hub`. This allows for seamless model updates without re-deploying the entire codebase.

### Why CatBoost?

- **Categorical features:** Native handling of categorical variables removes the need for complex pre-processing.
- **Robustness:** Built-in ordered boosting prevents target leakage and overfitting.
- **Inference speed:** Binary `.cbm` files are highly optimized for fast, real-time predictions.

### Why FastAPI?

- **High Performance:** Async support for concurrent request handling.
- **Type Safety:** Pydantic validation ensures incoming payloads match the expected schema.
- **Documentation:** Auto-generated Swagger UI simplifies integration.

## Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 98.72% |
| ROC AUC Score | 0.9888 |

## Repository Structure

```
customer-churn-mlops-pipeline/
├── .github/workflows/main.yml    # CI/CD pipeline
├── app/
│   ├── inference/predict.py      # Dynamic model fetching & inference
│   ├── routes/api.py             # API endpoints
│   └── schemas/request_body.py   # Pydantic models
├── notebooks/                    # EDA and training experiments
├── pipelines/                    # Data transformation logic
├── sql/                          # SQL queries for data ingestion
├── tests/                        # Pytest suite
├── Dockerfile                    # Containerization
└── pyproject.toml                # Dependency management (uv)
```

## Local Setup

Ensure you have Python 3.12 and `uv` installed.

```bash
# Install dependencies
uv sync --frozen

# Start local API
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker Deployment

```bash
docker build -t customer-churn-api .
docker run -p 8000:8000 -e DB_HOST=... -e DB_USER=... customer-churn-api
```

## Environment Variables

For production deployment, ensure the following variables are configured in your hosting environment:

| Variable | Description |
|----------|-------------|
| `DB_HOST` | Database host |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DB_PORT` | Database port |