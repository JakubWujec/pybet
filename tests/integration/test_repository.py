from src.pybet import repository
from src.pybet import schema
from sqlalchemy.sql import text
import pytest


@pytest.fixture
def setup_match_and_bet(session):
    session.execute(
        text(
            "INSERT INTO matches (id, home_team_id, away_team_id, gameround)"
            " VALUES (1, 1, 2, 1)"
        )
    )
    session.execute(
        text(
            "INSERT INTO bets (user_id, match_id, home_team_score, away_team_score)"
            " VALUES (1, 1, 3, 3)"
        )
    )
    session.commit()

def test_repository_can_retrieve_match(session, setup_match_and_bet):
    repo = repository.SqlMatchRepository(session)
    match = repo.get(match_id=1)
    assert match is not None
    assert isinstance(match, schema.Match)
    assert match.kickoff is not None

def test_repository_can_retrieve_match_and_user_bet(session, setup_match_and_bet):
    user_id = 1
    repo = repository.SqlMatchRepository(session)
    match: schema.Match = repo.get(match_id=1)

    bet = match.bets[user_id]
    assert bet.home_team_score == 3
    assert bet.away_team_score == 3