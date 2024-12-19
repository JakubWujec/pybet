import os
from src.config import Config

def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"

def get_sqlite_uri():
    return Config.SQLALCHEMY_DATABASE_URI