import abc
from src.pybet import model

class MatchRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, match: model.Match):
        raise NotImplementedError
        
    @abc.abstractmethod
    def get(self, match_id: int) -> model.Match:
        raise NotImplementedError 


class FakeMatchRepository:
    def __init__(self):
        self.matches = {}
        self._next_id = 1
        
    def add(self, match: model.Match):
        if match.id is None:
            match.id = self._next_id
            self._next_id +=1 
        self.matches[match.id] = match
        
    def get(self, match_id: int):
        return self.matches[match_id]    


class SqlMatchRepository:
    def __init__(self, session):
        super().__init__()
        self.session = session
    
    def add(self, match: model.Match):
        self.session.add(match)
    
    def get(self, match_id: int):
        return self.session.query(model.Match).filter_by(id=match_id).first()