from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    RAW_DATA_TRAINING_PATH: str = "data/raw/customer_churn_dataset-training-master.csv"
    RAW_DATA_TESTING_PATH: str = "data/raw/customer_churn_dataset-testing-master.csv"
    PROCESSED_DATA_PATH: str = "data/processed/churn_cleaned.csv"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()