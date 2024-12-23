import os 
from dotenv import load_dotenv
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy import create_engine
from src.pybet import schema
from contextlib import contextmanager
from sqlalchemy.pool import NullPool

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

# Private variables to hold the singleton instance
_session_factory = None  
_db_engine = None

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 280}
    ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN") or "admin"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "admin"
    PYTHON_ANYWHERE_MAX_CONNECTION_POOL = 6
    MAX_CONNECTION_POOL = os.environ.get("MAX_CONNECTION_POOL") or PYTHON_ANYWHERE_MAX_CONNECTION_POOL
    
def get_db_uri():
    return Config.SQLALCHEMY_DATABASE_URI

def get_session_factory() -> sessionmaker:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(bind=create_engine(get_db_uri()))
    return _session_factory

def get_session():
    return get_session_factory()()

def get_db_engine():
    global _db_engine
    if _db_engine is None:
        _db_engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True, poolclass=NullPool)
    return _db_engine

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = get_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()