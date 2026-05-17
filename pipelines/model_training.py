import os
import sys
import pandas as pd
import yaml
import mlflow
import mlflow.catboost

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from config.settings import settings
from utils.loggers_config import logger
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split

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
    
    if 'churn' in df.columns:
        target = 'churn'
    elif 'Churn' in df.columns:
        target = 'Churn'
    else:
        raise KeyError("Target column ('churn' or 'Churn') not found in the dataset!")

    df = df.reset_index(drop=True)

    if df[target].isnull().sum() > 0:
        logger.warning(f"Target '{target}' contained {df[target].isnull().sum()} NaN values! Dropping them now.")
        df = df.dropna(subset=[target])
        df = df.reset_index(drop=True)

    X = df.drop(columns=[target])
    y = df[target].astype(int) 

    X = X.fillna(0)
    
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
            
            model = CatBoostClassifier(**params)
            model.fit(X_train, y_train, eval_set=(X_val, y_val), early_stopping_rounds=50)

            mlflow.log_params(params)
            mlflow.log_metric("train_accuracy", model.score(X_train, y_train))
            mlflow.log_metric("validation_accuracy", model.score(X_val, y_val))

            mlflow.catboost.log_model(
                cb_model=model, 
                name="model", 
                pip_requirements=["catboost", "pandas", "numpy"]
            )
            
            os.makedirs("models", exist_ok=True)
            model.save_model("models/catboost_churn_model.cbm")
            logger.info("Model training and logging completed successfully.")

    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise e

if __name__ == "__main__":
    train_pipeline()