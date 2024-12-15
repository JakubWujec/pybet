from src.pybet.domain import model

def make_bet(match_id: int, home_team_score: int, away_team_score: int):
    # fetch match
    # check time
    # create bet
    # save in db
    
    bet = model.Bet(home_team_score, away_team_score)
    return bet