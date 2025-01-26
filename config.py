import os 
from dotenv import load_dotenv
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager

basedir = os.path.abspath(os.path.dirname(__file__))
chosen_env = os.environ.get('FLASK_ENV_FILE', '.env')
load_dotenv(os.path.join(basedir, chosen_env))
# Private variables to hold the singleton instance
_session_factory = None  
_db_engine = None

class Config:
    POINTS_FOR_EXACT_SCORE = os.environ.get('POINTS_FOR_EXACT_SCORE') or 5
    POINTS_FOR_DRAW = os.environ.get('POINTS_FOR_DRAW') or 3
    POINTS_FOR_WINNER = os.environ.get('POINTS_FOR_WINNER') or 2
    POINTS_FOR_MISS = os.environ.get('POINTS_FOR_WINNER') or 0
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 280}
    ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN") or "admin"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "admin"
    PYTHON_ANYWHERE_MAX_CONNECTION_POOL = 6
    MAX_CONNECTION_POOL = os.environ.get("MAX_CONNECTION_POOL") or PYTHON_ANYWHERE_MAX_CONNECTION_POOL
    
def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"

def get_sqlite_uri():
    return Config.SQLALCHEMY_DATABASE_URI
    
def get_db_uri():
    return Config.SQLALCHEMY_DATABASE_URI

def get_session_factory() -> sessionmaker:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_db_engine())
    return _session_factory

def get_session():
    return get_session_factory()()

# 'pool_size':  # Maximum of 4 persistent connections
# 'max_overflow': # No additional temporary connections
# 'pool_timeout': 10,     # Wait up to 10 seconds for a connection
# 'pool_recycle': 3600     # Recycle connections every hour (to avoid stale connections)
# 'pool_preping' 
def get_db_engine():
    global _db_engine
    if _db_engine is None:
        _db_engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_size=4, max_overflow=2, pool_timeout=5, pool_recycle=3600, pool_pre_ping=True)
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