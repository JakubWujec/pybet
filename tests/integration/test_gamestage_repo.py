from pybet.repositories import (
    GamestageRepository,
    FakeGamestageRepository,
    SqlGamestageRepository,
)
from pybet import schema
from sqlalchemy.sql import text
import pytest


@pytest.fixture
def setup_gamestage_and_match(session):
    session.execute(text("INSERT INTO gamestages (id, name) VALUES (1, 'Gameweek 1')"))

    session.execute(text("INSERT INTO teams (id, name) VALUES (1, 'ARS'), (2, 'CHE')"))
    session.execute(
        text(
            "INSERT INTO matches (id, home_team_id, away_team_id, gameround, gamestage_id)"
            " VALUES (1, 1, 2, 1, 1)"
        )
    )

    session.commit()


def test_repository_can_retrieve_gamestage(session, setup_gamestage_and_match):
    repo = SqlGamestageRepository(session)
    gamestage = repo.get(gamestage_id=1)

    assert gamestage is not None
    assert isinstance(gamestage, schema.Gamestage)
