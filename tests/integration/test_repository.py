from pybet import repository
from pybet import schema
from sqlalchemy.sql import text
import pytest


@pytest.fixture
def setup_match_and_bet(session):
    session.execute(text("INSERT INTO teams (id, name) VALUES (1, 'ARS'), (2, 'CHE')"))
    session.execute(
        text(
            "INSERT INTO matches (id, home_team_id, away_team_id, gameround, gamestage_id)"
            " VALUES (1, 1, 2, 1, 1)"
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


def test_repository_retrieve_match_with_teams_loaded(session, setup_match_and_bet):
    repo = repository.SqlMatchRepository(session)
    match = repo.get(match_id=1)

    assert match.home_team is not None
    assert match.away_team is not None
    assert match.home_team.name == "ARS"
    assert match.away_team.name == "CHE"


def test_repository_retrieve_matches__with_teams_loaded(session, setup_match_and_bet):
    repo = repository.SqlMatchRepository(session)
    matches = repo.get_gamestage_matches(gamestage_id=1)
    match = matches[0]

    assert match.home_team is not None
    assert match.away_team is not None
    assert match.home_team.name == "ARS"
    assert match.away_team.name == "CHE"


def test_repository_can_retrieve_match_and_user_bet(session, setup_match_and_bet):
    user_id = 1
    repo = repository.SqlMatchRepository(session)
    match: schema.Match = repo.get(match_id=1)

    bet = match.bets[user_id]
    assert bet.home_team_score == 3
    assert bet.away_team_score == 3
