import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw data by converting contract strings to numeric durations
    and applying One-Hot Encoding for remaining categorical variables.
    """
    df_clean = df.copy()
    
    # 1. Convert Contract Length from string categories to numeric months
    if "Contract Length" in df_clean.columns:
        # Standardize strings to lower case for exact mapping
        contract_map = {
            'monthly': 1,
            'quarterly': 3,
            'annual': 12
        }
        df_clean["Contract Length"] = df_clean["Contract Length"].astype(str).str.strip().str.lower().map(contract_map).fillna(1)
        
    # 2. Drop CustomerID if present
    if "CustomerID" in df_clean.columns:
        df_clean = df_clean.drop(columns=["CustomerID"])
        
    # 3. Apply One-Hot Encoding for the remaining object/string columns (e.g., Gender, Subscription Type)
    df_clean = pd.get_dummies(df_clean, drop_first=True)
    
    # 4. Explicitly convert boolean dummies to integer 0/1 signatures
    for col in df_clean.columns:
        if df_clean[col].dtype == 'bool':
            df_clean[col] = df_clean[col].astype(int)
            
    return df_clean

def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates engineered flags and standardized segment metrics.
    """
    df_fe = df.copy()
    
    df_fe['is_critical_payment_delay'] = (df_fe.get('Payment Delay', 0) > 20).astype(np.int32)
    df_fe['is_low_spender'] = (df_fe.get('Total Spend', 0) < 300).astype(np.int32)
    df_fe['high_support_risk'] = (df_fe.get('Support Calls', 0) > 5).astype(np.int32)
    df_fe['is_passive_user'] = (df_fe.get('Last Interaction', 0) > 25).astype(np.int32)
    df_fe['is_low_usage'] = (df_fe.get('Usage Frequency', 0) < 5).astype(np.int32)
    df_fe['tenure_segment'] = (df_fe.get('Tenure', 0) // 12).astype(np.int32)
    
    return df_fe