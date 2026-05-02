import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    datasets = {
        "train": "data/raw/customer_churn_dataset-training-master.csv",
        "test": "data/raw/customer_churn_dataset-testing-master.csv"
    }
    
    try:
        for mode, path in datasets.items():
            if not os.path.exists(path):
                print(f"File not found: {path}")
                continue
            
            df = pd.read_csv(path)
            table_name = f"raw_churn_{mode}"
            
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Successfully loaded {mode} data to '{table_name}' ({len(df)} rows).")
            
        print("\nData ingestion process completed successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ingest_data()