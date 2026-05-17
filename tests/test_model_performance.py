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
    
    if not os.path.exists(model_path):
        pytest.skip("Model file not found locally. Skipping performance test.")

    test_df = pd.read_csv(fixture_path)
    model = CatBoostClassifier()
    model.load_model(model_path)
    
    target_col = 'churn' if 'churn' in test_df.columns else 'Churn'
    y_test = test_df[target_col].fillna(0).astype(int)
    
    X_raw = test_df.drop(columns=[target_col])
    X_transformed = pd.get_dummies(X_raw, drop_first=True)
    
    model_features = model.feature_names_
    X_test = X_transformed.reindex(columns=model_features, fill_value=0)
    
    for col in X_test.columns:
        if X_test[col].dtype == 'bool':
            X_test[col] = X_test[col].astype(int)
            
    X_test = X_test.fillna(0)
    
    accuracy = model.score(X_test, y_test)
    assert accuracy >= 0.4, f"Model performance is too low: {accuracy}"