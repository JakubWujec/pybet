import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src import config
from src.pybet.schema import metadata
from pathlib import Path
from sqlalchemy.orm import Session
import time
import requests


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine

@pytest.fixture
def in_memory_sqlite_session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)

@pytest.fixture
def session(in_memory_sqlite_session_factory) -> Session:
    return in_memory_sqlite_session_factory()

@pytest.fixture
def sqlite_db():
    engine = create_engine(config.get_sqlite_uri())
    metadata.create_all(engine)
    return engine
    
def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")    
    
    

@pytest.fixture
def restart_api():
    (Path(__file__).parent.parent / "flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()