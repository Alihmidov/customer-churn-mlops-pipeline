from fastapi import FastAPI
from app.routes.api import router as api_router

app = FastAPI(
    title="Customer Churn Prediction Service",
    description="Production-ready FastAPI service that integrates a CatBoost machine learning model to predict customer churn.",
    version="1.0.0"
)

@app.get("/health", tags=["Monitoring"])
def health_check():
    return {"status": "healthy", "service": "customer-churn-mlops"}

app.include_router(api_router, prefix="/api/v1", tags=["Inference"])