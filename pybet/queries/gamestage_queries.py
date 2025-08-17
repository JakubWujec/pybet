from dataclasses import dataclass
from pybet.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy.sql import text
from datetime import datetime, timezone
from typing import List


@dataclass
class GamestageDTO:
    id: int
    name: str
    deadline: datetime


def get_all(uow: SqlAlchemyUnitOfWork) -> List[GamestageDTO]:
    with uow:
        gamestages = uow.gamestages.list()
        return [
            GamestageDTO(id=g.id, name=g.name, deadline=g.deadline) for g in gamestages
        ]
    return []


def get_current_gamestage(uow: SqlAlchemyUnitOfWork) -> GamestageDTO | None:
    gamestage_id = get_current_gamestage_id(uow)
    if gamestage_id is None:
        return None
    return get_by_id(gamestage_id=gamestage_id, uow=uow)


def get_by_id(gamestage_id: int, uow: SqlAlchemyUnitOfWork) -> GamestageDTO | None:
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
                " FROM ("
                " SELECT gamestage_id, MIN(kickoff) as gamestage_kickoff"
                " FROM matches"
                " GROUP BY gamestage_id) AS T1"
                " WHERE T1.gamestage_kickoff > :current_timestamp"
                " ORDER BY gamestage_kickoff ASC"
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
