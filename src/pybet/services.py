from src.pybet import model
from src.pybet import repository

def make_bet(match_id: int, home_team_score: int, away_team_score: int, repo: repository.MatchRepository):
    # fetch match
    # check time
    # create bet
    # save in db
    _match = repo.get(match_id)
    
    bet = model.Bet(match_id, home_team_score, away_team_score)
    return bet