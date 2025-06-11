import abc
from typing import List, Set

from sqlalchemy.orm import Session

from pybet import schema


class GamestageRepository(abc.ABC):
    def __init__(self):
        self.seen: Set[schema.Gamestage] = set()

    def add(self, gamestage: schema.Gamestage):
        self._add(gamestage)
        self.seen.add(gamestage)

    def get(self, gamestage_id: int) -> schema.Gamestage:
        gamestage = self._get(gamestage_id)
        if gamestage:
            self.seen.add(gamestage)
        return gamestage

    @abc.abstractmethod
    def list(self) -> List[schema.Gamestage]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_gamestage_matches(self, gamestage_id: int) -> List[schema.Match]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, gamestage: schema.Gamestage):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, gamestage_id) -> schema.Gamestage:
        raise NotImplementedError


class FakeGamestageRepository(GamestageRepository):
    def __init__(self):
        super().__init__()
        self.gamestages = {}
        self._next_id = 1

    def _add(self, gamestage: schema.Gamestage):
        if gamestage.id is None:
            gamestage.id = self._next_id
            self._next_id += 1
        self.gamestages[gamestage.id] = gamestage

    def _get(self, gamestage_id: int) -> schema.Gamestage:
        return self.gamestages[gamestage_id]

    def list(self):
        return list(self.gamestages.values())

    def get_gamestage_matches(self, gamestage_id: int):
        return list(
            filter(lambda m: m.gamestage_id == gamestage_id, self.gamestages.values())
        )


class SqlGamestageRepository(GamestageRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def _add(self, gamestage: schema.Gamestage):
        self.session.add(gamestage)

    def _get(self, gamestage_id: int):
        return self.session.query(schema.Gamestage).filter_by(id=gamestage_id).first()

    def get_gamestage_matches(self, gamestage_id: int):
        gamestage = self._get(gamestage_id=gamestage_id)
        if gamestage is None:
            return []
        return gamestage.matches

    def list(self):
        return self.session.query(schema.Gamestage).all()
