from src.pybet import model
from src.pybet import repository

def make_bet(user_id: int, match_id: int, home_team_score: int, away_team_score: int, repo: repository.MatchRepository, session):
    match = repo.get(match_id)    
    match.place_bet(user_id, home_team_score, away_team_score)
    session.commit()
    
    return match.id