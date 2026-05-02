from sqlalchemy import create_engine
from config.settings import settings

def get_db_engine():
    """
    Create a SQLAlchemy engine using the database connection parameters from settings.
    
    """ 
    connection_uri = (
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    
    return create_engine(connection_uri)