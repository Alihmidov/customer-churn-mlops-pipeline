import os
import sys
import pytest
import pandas as pd
from catboost import CatBoostClassifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

def test_model_training_output():
    model_path = "models/catboost_churn_model.cbm"
    
    assert os.path.exists(model_path), f"Model file not found at {model_path}! Training might have failed."
    
    try:
        model = CatBoostClassifier()
        model.load_model(model_path)
    except Exception as e:
        pytest.fail(f"Failed to load the trained model file: {e}")


def test_model_evaluation_metrics():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample_testing.csv")
    model_path = "models/catboost_churn_model.cbm"
    
    test_df = pd.read_csv(fixture_path)
    model = CatBoostClassifier()
    model.load_model(model_path)
    
    target_col = 'churn' if 'churn' in test_df.columns else 'Churn'
    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]
    
    accuracy = model.score(X_test, y_test)
    
    min_accuracy_threshold = 0.75
    assert accuracy >= min_accuracy_threshold, f"Model accuracy ({accuracy:.4f}) is below the threshold ({min_accuracy_threshold})!"