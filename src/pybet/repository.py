import abc
from src.pybet import schema
from typing import List

class MatchRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, match: schema.Match):
        raise NotImplementedError
        
    @abc.abstractmethod
    def get(self, match_id: int) -> schema.Match:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def list(self) -> List[schema.Match]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_gameround_matches(self, gameround: int):
        raise NotImplementedError

class FakeMatchRepository:
    def __init__(self):
        self.matches = {}
        self._next_id = 1
        
    def add(self, match: schema.Match):
        if match.id is None:
            match.id = self._next_id
            self._next_id +=1 
        self.matches[match.id] = match
        
    def get(self, match_id: int) -> schema.Match:
        return self.matches[match_id]   

    def list(self):
        return list(self.matches.values())

    def get_gameround_matches(self, gameround: int):
        return list(
            filter(
                lambda m: m.gameround == gameround,
                self.matches.values()
            )
        )


class SqlMatchRepository:
    def __init__(self, session):
        super().__init__()
        self.session = session
    
    def add(self, match: schema.Match):
        self.session.add(match)
        self.session.commit()
    
    def get(self, match_id: int):
        return self.session.query(schema.Match).filter_by(id=match_id).first()
    
    def get_gameround_matches(self, gameround: int):
        return self.session.query(schema.Match).filter_by(gameround=gameround).all()
    
    def list(self):
        return self.session.query(schema.Match).all()