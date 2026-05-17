import os
import sys
import pytest
import pandas as pd
from catboost import CatBoostClassifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from pipelines.data_transformation import clean_data, apply_feature_engineering

def test_model_training_output():
    """Verifies the physical existence and state of the saved CatBoost model."""
    model_path = "models/catboost_churn_model.cbm"
    assert os.path.exists(model_path), f"Model file not found at: {model_path}"

def test_model_evaluation_metrics():
    """Validates production matrix compatibility and checks target performance thresholds."""
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample_testing.csv")
    model_path = "models/catboost_churn_model.cbm"
    
    if not os.path.exists(model_path):
        pytest.skip("Model file not found locally. Skipping performance test.")

    test_df = pd.read_csv(fixture_path)
    model = CatBoostClassifier()
    model.load_model(model_path)
    
    target_lookup = {col.lower().strip(): col for col in test_df.columns}
    if 'churn' in target_lookup:
        y_test = test_df[target_lookup['churn']].fillna(0).astype(int)
    else:
        pytest.fail("Target column 'Churn' not found in test fixture.")
    
    cleaned_df = clean_data(test_df)
    if target_lookup['churn'] in cleaned_df.columns:
        cleaned_df = cleaned_df.drop(columns=[target_lookup['churn']])
        
    final_df = apply_feature_engineering(cleaned_df)
    
    model_features = [
        'Age', 'Tenure', 'Usage Frequency', 'Support Calls', 'Payment Delay', 'Contract Length', 
        'Total Spend', 'Last Interaction', 'Gender_male', 'Subscription Type_premium', 
        'Subscription Type_standard', 'is_critical_payment_delay', 'is_low_spender', 
        'high_support_risk', 'is_passive_user', 'is_low_usage', 'tenure_segment'
    ]
    
    X_test = pd.DataFrame(0, index=final_df.index, columns=model_features)
    final_df_map = {col.lower().strip(): col for col in final_df.columns}
    
    for feature in model_features:
        feature_lower = feature.lower().strip()
        if feature_lower in final_df_map:
            X_test[feature] = final_df[final_df_map[feature_lower]]
        elif feature == 'Gender_male':
            gender_col = final_df_map.get('gender')
            if gender_col:
                X_test['Gender_male'] = (final_df[gender_col].astype(str).str.title() == 'Male').astype(int)
        elif feature == 'Subscription Type_premium':
            sub_col = final_df_map.get('subscription type')
            if sub_col:
                X_test['Subscription Type_premium'] = (final_df[sub_col].astype(str).str.title() == 'Premium').astype(int)
        elif feature == 'Subscription Type_standard':
            sub_col = final_df_map.get('subscription type')
            if sub_col:
                X_test['Subscription Type_standard'] = (final_df[sub_col].astype(str).str.title() == 'Standard').astype(int)          
                
    accuracy = model.score(X_test, y_test)
    assert accuracy >= 0.90, f"Model accuracy on real 100-row fixture is lower than expected: {accuracy}"