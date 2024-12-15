import abc
from src.pybet.domain import model

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
