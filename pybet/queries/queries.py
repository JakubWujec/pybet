from dataclasses import dataclass
from pybet.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy.sql import text
from datetime import datetime, timezone
from typing import List


def mygamestage(user_id: int, gamestage_id: int, uow: SqlAlchemyUnitOfWork):
    with uow:
        rows = list(
            uow.session.execute(
                text("""
            SELECT 
                m.id, 
                ht.id, 
                ht.name, 
                at.id, 
                at.name, 
                m.home_team_score, 
                m.away_team_score, 
                kickoff, 
                b.id, 
                b.home_team_score, 
                b.away_team_score, 
                b.points
            FROM matches AS m
            JOIN teams as ht ON ht.id = m.home_team_id
            JOIN teams as at ON at.id = m.away_team_id
            LEFT JOIN bets AS b on b.match_id = m.id AND b.user_id = :user_id
            WHERE m.gamestage_id = :gamestage_id
            ORDER by kickoff ASC"""),
                dict(user_id=user_id, gamestage_id=gamestage_id),
            )
        )
    result = {"matches": []}

    for (
        match_id,
        home_team_id,
        home_team_name,
        away_team_id,
        away_team_name,
        home_team_score,
        away_team_score,
        kickoff,
        bet_id,
        bet_home,
        bet_away,
        bet_points,
    ) in rows:
        match = {
            "id": match_id,
            "user_id": user_id,
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "home_team": {"id": home_team_id, "name": home_team_name},
            "away_team": {"id": away_team_id, "name": away_team_name},
            "kickoff": kickoff_to_datetime(kickoff),
            "home_team_score": home_team_score,
            "away_team_score": away_team_score,
            "bet": None,
        }
        if bet_id is not None:
            match["bet"] = {
                "id": bet_id,
                "home_team_score": bet_home,
                "away_team_score": bet_away,
                "points": bet_points,
            }
        result["matches"].append(match)

    return result


def get_username_by_user_id(user_id: int, uow: SqlAlchemyUnitOfWork) -> str | None:
    with uow:
        username = uow.session.execute(
            text("""SELECT username from users where id = :user_id"""),
            dict(user_id=user_id),
        ).scalar_one_or_none()
        return username


def kickoff_to_datetime(kickoff):
    if isinstance(kickoff, datetime):
        return kickoff
    return datetime.strptime(kickoff, "%Y-%m-%d %H:%M:%S.%f")


@dataclass
class StandingEntryDTO:
    user_id: int
    username: str
    points: int
    position: int


@dataclass
class StandingsQueryResultDTO:
    standings: List[StandingEntryDTO]
    count: int


def standings_query(
    gamestage_id: int, page: int, per_page: int, uow: SqlAlchemyUnitOfWork
) -> StandingsQueryResultDTO:
    offset = (page - 1) * per_page
    with uow:
        count: int = uow.session.execute(
            text(
                """
                SELECT COUNT(DISTINCT u.id)
                FROM users as u
                JOIN bets as b on b.user_id = u.id
                JOIN matches as m on m.id = b.match_id
                WHERE m.gamestage_id = :gamestage_id
            """
            ),
            dict(gamestage_id=gamestage_id),
        ).scalar_one()

        rows = uow.session.execute(
            text(
                """
                SELECT u.id id, u.username username, SUM(b.points) points, RANK() OVER(ORDER BY SUM(b.points) DESC) position
                FROM users as u
                JOIN bets as b on b.user_id = u.id
                JOIN matches as m on m.id = b.match_id
                WHERE m.gamestage_id = :gamestage_id
                GROUP BY u.id, u.username
                LIMIT :limit OFFSET :offset;
            """
            ),
            dict(gamestage_id=gamestage_id, limit=per_page, offset=offset),
        ).all()

    standings = list(
        map(
            lambda row: StandingEntryDTO(
                user_id=row[0], username=row[1], points=row[2], position=row[3]
            ),
            rows,
        )
    )

    return StandingsQueryResultDTO(count=count, standings=standings)
