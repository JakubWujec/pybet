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
class GamestageDTO:
    id: int
    name: str
    deadline: datetime


def get_gamestage_by_id(
    gamestage_id: int, uow: SqlAlchemyUnitOfWork
) -> GamestageDTO | None:
    with uow:
        gamestage = uow.gamestages.get(gamestage_id=gamestage_id)
        return GamestageDTO(
            id=gamestage.id, name=gamestage.name, deadline=gamestage.deadline
        )
    return None


def get_previous_gamestage_id(uow: SqlAlchemyUnitOfWork):
    current_timestamp = datetime.now()

    with uow:
        gamestage_id = uow.session.execute(
            text(
                "SELECT gamestage_id"
                " FROM matches AS m"
                " WHERE kickoff <= :current_timestamp"
                " ORDER BY kickoff DESC"
                " LIMIT 1"
            ),
            dict(current_timestamp=current_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")),
        ).scalar()

        return gamestage_id


def get_current_gamestage_id(uow: SqlAlchemyUnitOfWork):
    current_timestamp = datetime.now()

    with uow:
        gamestage_id = uow.session.execute(
            text(
                "SELECT gamestage_id"
                " FROM matches AS m"
                " WHERE kickoff > :current_timestamp"
                " ORDER BY kickoff ASC"
                " LIMIT 1"
            ),
            dict(current_timestamp=current_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")),
        ).scalar()

        return gamestage_id


def get_gamestage_id_by_date(date: datetime, uow: SqlAlchemyUnitOfWork):
    with uow:
        result = uow.session.execute(
            text(
                "SELECT MAX(gamestage_id)"
                " FROM matches AS m"
                " WHERE kickoff <= :current_timestamp"
            ),
            dict(current_timestamp=date.strftime("%Y-%m-%d %H:%M:%S.%f")),
        ).scalar()
        return result


def get_available_gamestage_ids(uow: SqlAlchemyUnitOfWork) -> List[int]:
    with uow:
        result = uow.session.execute(
            text("SELECT id FROM gamestages ORDER BY id")
        ).all()
        return [row[0] for row in result]


def standings_query(
    gamestage_id: int, page: int, per_page: int, uow: SqlAlchemyUnitOfWork
):
    offset = (page - 1) * per_page
    with uow:
        count = uow.session.execute(
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
        ).scalar()

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
            lambda row: {
                "user_id": row[0],
                "username": row[1],
                "points": row[2],
                "position": row[3],
            },
            rows,
        )
    )

    return {
        "standings": standings,
        "count": count,
    }
