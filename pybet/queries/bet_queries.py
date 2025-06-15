from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

from sqlalchemy.sql import text

from pybet.unit_of_work import SqlAlchemyUnitOfWork
from pybet.services import (
    calculate_points,
    calculate_points_for_score,
    calculate_points_for_result,
)


@dataclass
class BetDTO:
    id: int
    user_id: int
    match_id: int
    home_team_score: int
    away_team_score: int
    result_points: int
    score_points: int
    total_points: int


def get_user_gamestage_bets(
    user_id: int, gamestage_id: int, uow: SqlAlchemyUnitOfWork
) -> List[BetDTO]:
    with uow:
        rows = list(
            uow.session.execute(
                text("""
            SELECT 
                m.id as match_id,
                m.home_team_score,
                m.away_team_score,
                b.id as bet_id,
                b.user_id as user_id,
                b.home_team_score, 
                b.away_team_score
            FROM matches AS m
            LEFT JOIN bets AS b on b.match_id = m.id AND b.user_id = :user_id
            WHERE m.gamestage_id = :gamestage_id
            ORDER by kickoff ASC"""),
                dict(user_id=user_id, gamestage_id=gamestage_id),
            )
        )
        betDTOS = []
        for (
            match_id,
            match_home_score,
            match_away_score,
            bet_id,
            user_id,
            bet_home_score,
            bet_away_score,
        ) in rows:
            if bet_id is None:
                continue
            result_points = 0
            score_points = 0
            if match_home_score is not None and match_away_score is not None:
                result_points = calculate_points_for_result(
                    bet_home_score=bet_home_score,
                    bet_away_score=bet_away_score,
                    match_away_score=match_away_score,
                    match_home_score=match_home_score,
                )

                score_points = calculate_points_for_score(
                    bet_home_score=bet_home_score,
                    bet_away_score=bet_away_score,
                    match_away_score=match_away_score,
                    match_home_score=match_home_score,
                )

            betDTO = BetDTO(
                id=bet_id,
                user_id=user_id,
                match_id=match_id,
                home_team_score=bet_home_score,
                away_team_score=bet_away_score,
                result_points=result_points,
                score_points=score_points,
                total_points=score_points + result_points,
            )
            betDTOS.append(betDTO)

        return betDTOS
