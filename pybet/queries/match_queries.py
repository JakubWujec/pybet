from dataclasses import dataclass
from datetime import datetime
from typing import List

from pybet.unit_of_work import SqlAlchemyUnitOfWork


@dataclass
class MatchDto:
    id: int
    home_team_id: int
    away_team_id: int
    gamestage_id: int
    home_team_name: str
    away_team_name: str
    home_team_score: int
    away_team_score: int
    kickoff: datetime


def get_by_gamestage_id(gamestage_id: int, uow: SqlAlchemyUnitOfWork) -> List[MatchDto]:
    with uow:
        matches = uow.matches.get_gamestage_matches(gamestage_id)
        result = [
            MatchDto(
                id=m.id,
                home_team_id=m.home_team_id,
                away_team_id=m.away_team_id,
                home_team_name=m.home_team.name,
                away_team_name=m.away_team.name,
                home_team_score=m.home_team_score,
                away_team_score=m.away_team_score,
                kickoff=m.kickoff,
                gamestage_id=m.gamestage_id,
            )
            for m in matches
        ]

        return result
