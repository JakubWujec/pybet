from sqlalchemy.orm.session import Session, sessionmaker
from src.pybet.repository import SqlMatchRepository, MatchRepository
import abc 
from sqlalchemy import create_engine
from src.pybet import config

class UnitOfWork(abc.ABC):
    matches: MatchRepository
    
    def __enter__(self):
        pass
    
    def __exit__(self, *args):
        self.rollback()
        
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(config.get_sqlite_uri()))

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker = DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
    
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.matches = SqlMatchRepository(self.session)
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
        
    def commit(self):
        self.session.commit()
        
    def rollback(self):
        self.session.rollback()