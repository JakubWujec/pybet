import os 
from dotenv import load_dotenv
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy import create_engine
from src.pybet import schema
from contextlib import contextmanager

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))
_session_factory = None  # Private variable to hold the singleton instance

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 280}
    ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN") or "admin"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "admin"
    
def get_db_uri():
    return Config.SQLALCHEMY_DATABASE_URI

def get_session_factory() -> sessionmaker:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(bind=create_engine(get_db_uri()))
    return _session_factory

def get_session():
    return get_session_factory()()

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