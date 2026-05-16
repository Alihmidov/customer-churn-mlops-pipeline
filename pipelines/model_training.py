import os
import sys
import pandas as pd
import yaml
import mlflow
import mlflow.catboost
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from config.settings import settings
from utils.loggers_config import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

def load_hyperparameters():
    try:
        with open("config/hyperparams.yaml", "r") as f:
            config = yaml.safe_load(f)
        return config.get("catboost", {})
    except Exception:
        logger.warning("Hyperparams file not found. Using defaults.")
        return {"iterations": 500, "learning_rate": 0.05, "depth": 6}

def get_prepared_data():
    df = pd.read_csv("data/processed/engineered_churn_data.csv")
    
    target = 'churn' if 'churn' in df.columns else 'Churn'
    X = df.drop(columns=[target])
    y = df[target]
    
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def train_pipeline():
    try:
        tracking_uri = settings.MLFLOW_TRACKING_URI if hasattr(settings, 'MLFLOW_TRACKING_URI') else "sqlite:///mlflow.db"
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment("Customer_Churn_Training")

        X_train, X_val, y_train, y_val = get_prepared_data()
        params = load_hyperparameters()

        with mlflow.start_run(run_name="CatBoost_Production_Run"):
            logger.info("Starting model training...")
            
            model = CatBoostClassifier(**params, verbose=100, random_seed=42)
            model.fit(X_train, y_train, eval_set=(X_val, y_val), early_stopping_rounds=50)

            mlflow.log_params(params)
            mlflow.log_metric("train_accuracy", model.score(X_train, y_train))
            mlflow.log_metric("validation_accuracy", model.score(X_val, y_val))

            mlflow.catboost.log_model(model, artifact_path="model")
            
            os.makedirs("models", exist_ok=True)
            model.save_model("models/catboost_churn_model.cbm")
            logger.info("Model training and logging completed successfully.")

    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise e

if __name__ == "__main__":
    train_pipeline()