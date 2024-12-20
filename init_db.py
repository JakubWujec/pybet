from sqlalchemy import create_engine
from src.pybet.schema import metadata  # Replace with actual schema import
from src.config import Config  # Replace with actual config import

def initialize_database():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    metadata.create_all(engine)


if __name__ == "__main__":
    initialize_database()
