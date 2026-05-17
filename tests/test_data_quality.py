import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils.helpers import get_db_engine

def test_target_variable_integrity():
    engine = get_db_engine()
    df = pd.read_sql('SELECT "Churn" FROM processed_churn_data', engine)
    
    unique_values = set(df['Churn'].unique())
    assert unique_values.issubset({0, 1}), f"Data Quality Error: Invalid labels found: {unique_values}"
    
def test_critical_columns_presence():
    engine = get_db_engine()
    df = pd.read_sql("SELECT * FROM raw_train_data LIMIT 1", engine)
    required_columns = ['last interaction', 'support calls', 'gender', 'tenure', 'age']
    actual_columns = [col.lower() for col in df.columns]
    
    for col in required_columns:
        assert col in actual_columns, f"Data Quality Error: Missing critical column '{col}'"