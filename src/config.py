import os 
from dotenv import load_dotenv
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy import create_engine
from src.pybet import schema

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 280}
    
def get_db_uri():
    return Config.SQLALCHEMY_DATABASE_URI

def get_session_factory():
    return sessionmaker(bind=create_engine(get_db_uri()))

def get_session():
    return sessionmaker()

