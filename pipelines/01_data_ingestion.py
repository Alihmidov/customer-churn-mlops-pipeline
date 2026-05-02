import pandas as pd
from utils.helpers import get_db_engine
from config.settings import settings

def ingest_data():
    try:
        engine = get_db_engine()
        
        df_train = pd.read_csv(settings.RAW_DATA_TRAINING_PATH)
        df_train.to_sql("raw_train_data", engine, if_exists="replace", index=False)
        print("Train data loaded.")

        df_test = pd.read_csv(settings.RAW_DATA_TESTING_PATH)
        df_test.to_sql("raw_test_data", engine, if_exists="replace", index=False)
        print("Test data loaded.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ingest_data()