import abc
from pybet import schema
from typing import List, Set
from sqlalchemy.orm import Session, joinedload

class MatchRepository(abc.ABC):
    def __init__(self):
        self.seen: Set[schema.Match] = set()
        
    def add(self, match: schema.Match):
        self._add(match)
        self.seen.add(match)
        
    def get(self, match_id: int) -> schema.Match:
        match = self._get(match_id)
        if match:
            self.seen.add(match)
        return match
    
    @abc.abstractmethod
    def list(self) -> List[schema.Match]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_gameround_matches(self, gameround: int) -> List[schema.Match]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def _add(self, match: schema.Match):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _get(self, match_id) -> schema.Match:
        raise NotImplementedError

class FakeMatchRepository(MatchRepository):
    def __init__(self):
        super().__init__()
        self.matches = {}
        self._next_id = 1
        
    def _add(self, match: schema.Match):
        if match.id is None:
            match.id = self._next_id
            self._next_id +=1 
        self.matches[match.id] = match
        
    def _get(self, match_id: int) -> schema.Match:
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


class SqlMatchRepository(MatchRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session
    
    def _add(self, match: schema.Match):
        self.session.add(match)
    
    def _get(self, match_id: int):
        return self.session.query(schema.Match).filter_by(id=match_id).first()
    
    def get_gameround_matches(self, gameround: int):
        result = self.session.query(schema.Match) \
            .options(joinedload(schema.Match.home_team)) \
            .options(joinedload(schema.Match.away_team)) \
            .filter(
                schema.Match.gameround==gameround
            ).all()
        
        return result
    
    def list(self):
        return self.session.query(schema.Match).all()