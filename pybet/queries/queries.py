from dataclasses import dataclass
from pybet.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy.sql import text
from datetime import datetime, timezone
from typing import List


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
