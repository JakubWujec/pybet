from sqlalchemy.orm.session import Session, sessionmaker
from src.pybet.repository import SqlMatchRepository, MatchRepository
import abc 
from src import config

class UnitOfWork(abc.ABC):
    matches: MatchRepository
    
    def __enter__(self):
        pass
    
    def __exit__(self, *args):
        self.rollback()
                
    def collect_new_events(self):
        for match in self.matches.seen:
            while match.events:
                yield match.events.pop(0)
        
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker = None):
        if session_factory is None:
            session_factory = config.get_session_factory()
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