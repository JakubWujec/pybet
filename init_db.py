from sqlalchemy import create_engine
from src.pybet.schema import metadata
from src.config import Config 

def initialize_database():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    metadata.create_all(engine)

if __name__ == "__main__":
    initialize_database()
