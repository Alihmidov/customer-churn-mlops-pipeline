import os
from fastapi import FastAPI
# main.py kökdə olduğu üçün app/ qovluğundan bu cür import etməlidir:
from app.routes.api import router as api_router

ENV = os.getenv("ENV", "development")
MODEL_PATH = os.getenv("MODEL_PATH", "models/catboost_churn_model.cbm")

app = FastAPI(
    title="Customer Churn Prediction Service",
    description="Production-ready FastAPI service that integrates a CatBoost machine learning model to predict customer churn.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "healthy", 
        "service": "customer-churn-mlops",
        "environment": ENV,
        "model_path": MODEL_PATH  
    }

app.include_router(api_router, prefix="/api/v1", tags=["Inference"])