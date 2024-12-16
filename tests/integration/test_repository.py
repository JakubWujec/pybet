from src.pybet import repository
from src.pybet import model
from sqlalchemy.sql import text

def test_repository_can_retrieve_match(session):
    session.execute(
        text(
        "INSERT INTO matches (home_team_id, away_team_id)"
        ' VALUES (1, 2)')
    )
    
    session.execute(
        text(
        "INSERT INTO bets (user_id, match_id, home_team_score, away_team_score)"
        ' VALUES (1, 1, 3, 3)')
    )
    
    repo = repository.SqlMatchRepository(session)
    match = repo.get(match_id=1)
    
    assert match is not None
    assert isinstance(match, model.Match)
    
    
def test_repository_can_retrieve_match_and_user_bet(session):
    session.execute(
        text(
        "INSERT INTO matches (home_team_id, away_team_id)"
        ' VALUES (1, 2)')
    )
    
    session.execute(
        text(
        "INSERT INTO bets (user_id, match_id, home_team_score, away_team_score)"
        ' VALUES (1, 1, 3, 3)')
    )
    
    repo = repository.SqlMatchRepository(session)
    match: model.Match = repo.get(match_id=1)
    
    assert len(match.bets)
    assert isinstance(match.bets[0], model.Bet)
    assert match.bets[0].home_team_score == 3
    assert match.bets[0].away_team_score == 3
    
    
    