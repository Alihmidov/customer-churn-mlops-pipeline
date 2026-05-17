import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import pandas as pd
import json
import mlflow
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
import seaborn as sns
from config.settings import settings
from utils.loggers_config import logger

def get_prepared_data():
    df = pd.read_csv("data/processed/engineered_churn_data.csv")
    
    if 'churn' in df.columns:
        target = 'churn'
    elif 'Churn' in df.columns:
        target = 'Churn'
    else:
        raise KeyError("Target column not found!")

    df = df.reset_index(drop=True)
    df = df.dropna(subset=[target])
    
    X = df.drop(columns=[target]).fillna(0)
    y = df[target].astype(int)
    
    _, X_eval, _, y_eval = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    return X_eval, y_eval

def evaluate_model():
    try:
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI if hasattr(settings, 'MLFLOW_TRACKING_URI') else "sqlite:///mlflow.db")
        mlflow.set_experiment("Customer_Churn_Evaluation")

        model_path = "models/catboost_churn_model.cbm"
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Trained model not found at {model_path}. Run training first!")

        logger.info(f"Loading model from {model_path} for evaluation...")
        model = CatBoostClassifier()
        model.load_model(model_path)
        
        X_eval, y_eval = get_prepared_data()

        with mlflow.start_run(run_name="Model_Evaluation_Metrics"):
            logger.info("Generating predictions and computing evaluation metrics...")
            
            preds = model.predict(X_eval)
            pred_probs = model.predict_proba(X_eval)[:, 1]

            roc_auc = roc_auc_score(y_eval, pred_probs)
            report = classification_report(y_eval, preds, output_dict=True)
            
            mlflow.log_metric("eval_roc_auc", roc_auc)
            mlflow.log_metric("eval_precision_churn", report['1']['precision'])
            mlflow.log_metric("eval_recall_churn", report['1']['recall'])
            mlflow.log_metric("eval_f1_churn", report['1']['f1-score'])

            logger.info("Generating Confusion Matrix plot...")
            cm = confusion_matrix(y_eval, preds)
            plt.figure(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No Churn', 'Churn'], yticklabels=['No Churn', 'Churn'])
            plt.title('Confusion Matrix')
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            
            os.makedirs("models", exist_ok=True)
            plot_path = "models/confusion_matrix.png"
            plt.savefig(plot_path)
            plt.close()
            mlflow.log_artifact(plot_path)

            report_path = "models/classification_report.json"
            with open(report_path, "w") as f:
                json.dump(report, f, indent=4)
            mlflow.log_artifact(report_path)

            logger.info("Model evaluation completed. Artifacts logged to MLflow.")

    except Exception as e:
        logger.error(f"Error occurred during the model evaluation pipeline: {e}")
        raise e

if __name__ == "__main__":
    evaluate_model()