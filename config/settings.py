import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    RAW_DATA_TRAINING_PATH = r"data\raw\customer_churn_dataset-training-master.csv"
    RAW_DATA_TESTING_PATH = r"data\raw\customer_churn_dataset-testing-master.csv"
    PROCESSED_DATA_PATH = r"data\processed\customer_churn_dataset-testing-master.csv"

settings = Settings()