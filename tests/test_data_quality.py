import pandas as pd
import pytest
from utils.helpers import get_db_engine

def test_raw_data_loading():
    """
    Test if the raw data table exists in the database and is not empty.
    This validates the output of 01_data_ingestion.py.
    """
    engine = get_db_engine()
    
    query = "SELECT * FROM raw_train_data LIMIT 10"
    df = pd.read_sql(query, engine)
    
    assert not df.empty, "Data Quality Error: The raw_train_data table is empty."
    
def test_critical_columns_presence():
    """
    Check if the essential columns required for the Churn model are present.
    """
    engine = get_db_engine()
    query = "SELECT * FROM raw_train_data LIMIT 1"
    df = pd.read_sql(query, engine)
    
    required_columns = ['last interaction', 'support calls', 'gender', 'tenure', 'age']
    
    actual_columns = [col.lower() for col in df.columns]
    
    for col in required_columns:
        assert col in actual_columns, f"Data Quality Error: Missing critical column '{col}'"
        
def test_target_variable_integrity():
    
    engine = get_db_engine()
    query = 'SELECT "Churn" FROM raw_train_data' 
    df = pd.read_sql(query, engine)
    
    unique_values = set(df['Churn'].unique())

    assert unique_values.issubset({0, 1}), f"Data Quality Error: Invalid labels found: {unique_values}"
    
def test_data_row_count():
    """
    Verify that the ingestion process pulled a reasonable number of rows.
    Adjust the threshold based on your dataset size.
    """
    engine = get_db_engine()
    query = "SELECT COUNT(*) as row_count FROM raw_train_data"
    count = pd.read_sql(query, engine).iloc[0]['row_count']
    
    assert count > 5000, f"Data Quality Error: Expected >5000 rows, but found only {count}."