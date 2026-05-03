import pandas as pd
from config.settings import settings
from utils.helpers import get_db_engine
from utils.loggers_config import logger 

def ingest_data():
    """
    Reads raw CSV files and loads them into the PostgreSQL database.
    """
    try:
        engine = get_db_engine()
        logger.info("Database connection successful.") 

        df_train = pd.read_csv(settings.RAW_DATA_TRAINING_PATH)
        df_train.to_sql("raw_train_data", engine, if_exists="replace", index=False)
        logger.info(f"Train data loaded from {settings.RAW_DATA_TRAINING_PATH}")

        df_test = pd.read_csv(settings.RAW_DATA_TESTING_PATH)
        df_test.to_sql("raw_test_data", engine, if_exists="replace", index=False)
        logger.info(f"Test data loaded from {settings.RAW_DATA_TESTING_PATH}")

    except Exception as e:
        logger.error(f"Error occurred during data ingestion: {e}")

if __name__ == "__main__":
    ingest_data()