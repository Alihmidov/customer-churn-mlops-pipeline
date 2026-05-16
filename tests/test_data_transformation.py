import os
import sys
import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from pipelines.data_transformation import clean_data, apply_feature_engineering

@pytest.fixture
def real_sample_data():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample_training.csv")
    return pd.read_csv(fixture_path)

def test_data_transformation_pipeline(real_sample_data):
    cleaned_df = clean_data(real_sample_data)
    
    assert 'CustomerID' not in cleaned_df.columns, "CustomerID column was not dropped!"
    assert 'Gender_Male' in cleaned_df.columns or 'Gender_Female' in cleaned_df.columns, "Dummy columns for Gender were not created!"
    
    final_df = apply_feature_engineering(cleaned_df)
    
    expected_features = [
        'is_critical_payment_delay', 
        'is_low_spender', 
        'high_support_risk', 
        'is_passive_user', 
        'is_low_usage', 
        'tenure_segment'
    ]
    
    for feature in expected_features:
        assert feature in final_df.columns, f"Error: {feature} column was not added to the dataframe!"
        
    assert final_df['tenure_segment'].dtype in ['int32', 'int64'], "tenure_segment type is not integer!"
    assert final_df['high_support_risk'].dtype in ['int32', 'int64'], "high_support_risk type is not integer!"