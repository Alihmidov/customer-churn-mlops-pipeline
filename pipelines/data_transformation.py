import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from config.settings import settings
from utils.helpers import get_db_engine
from utils.loggers_config import logger 

def clean_data(df):
    logger.info("Starting data cleaning process.")
    df = df.copy()
    
    if 'CustomerID' in df.columns:
        df = df.drop(['CustomerID'], axis=1)
    
    target = 'churn' if 'churn' in df.columns else 'Churn'
    if target in df.columns:
        df = df.dropna(subset=[target])
    
    df['Contract Length'] = df['Contract Length'].replace('None', 0)

    target = 'churn' if 'churn' in df.columns else 'Churn'
    if target in df.columns:
        initial_count = len(df)
        df = df.dropna(subset=[target])
        logger.info(f"Target column cleaning: Dropped {initial_count - len(df)} rows containing NaN.")

    le = LabelEncoder()
    df['Contract Length'] = le.fit_transform(df['Contract Length'].astype(str))

    for col in ['Gender', 'Subscription Type']:
        if col in df.columns:
            df = pd.get_dummies(df, columns=[col], drop_first=True, dtype=int)

    return df

def apply_feature_engineering(df):
    logger.info("Starting feature engineering process...")
    df = df.copy()
    
    df['is_critical_payment_delay'] = (df['Payment Delay'] > 20).astype(int)
    df['is_low_spender'] = (df['Total Spend'] < 500).astype(int)
    
    def get_support_risk(row):
        if row['Age'] > 50: 
            return 1 
        if row['Age'] < 30 and row['Support Calls'] > 2: 
            return 1
        if 30 <= row['Age'] <= 50 and row['Support Calls'] > 5: 
            return 1
        return 0
    
    df['high_support_risk'] = df.apply(get_support_risk, axis=1)
    
    df['is_passive_user'] = (df['Last Interaction'] > 15).astype(int)
    df['is_low_usage'] = (df['Usage Frequency'] < 10).astype(int)
    
    max_tenure = max(df['Tenure'].max(), 61)
    
    df['tenure_segment'] = pd.cut(
        df['Tenure'], 
        bins=[0, 5, 11, 24, max_tenure], 
        labels=[1, 2, 3, 4],
        include_lowest=True
    )
    
    df['tenure_segment'] = df['tenure_segment'].fillna(1).astype(int)
    
    logger.info("Feature engineering completed successfully.") 
    return df

def transform_data():
    try:
        engine = get_db_engine()
        logger.info("Successfully connected to the database for transformation.")

        logger.info("Loading raw training data from PostgreSQL...")
        raw_df = pd.read_sql("SELECT * FROM raw_train_data", engine)

        cleaned_df = clean_data(raw_df)
        final_df = apply_feature_engineering(cleaned_df)

        final_df.to_sql("processed_churn_data", engine, if_exists="replace", index=False)
        logger.info("Processed data saved to PostgreSQL table 'processed_churn_data'.")

        output_path = "data/processed/engineered_churn_data.csv"
        final_df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved engineered data to {output_path}")

    except Exception as e:
        logger.error(f"Error occurred during data transformation pipeline: {e}")
        raise e

if __name__ == "__main__":
    transform_data()