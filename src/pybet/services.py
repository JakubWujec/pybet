from src.pybet import repository, schema

def make_bet(user_id: int, match_id: int, home_team_score: int, away_team_score: int, repo: repository.MatchRepository, session):
    match = repo.get(match_id)    
    bet = schema.Bet(
        user_id=user_id,
        home_team_score=home_team_score,
        away_team_score=away_team_score
    )    
    match.place_bet(bet)
    session.commit()
    
    return match.id


def update_match_score(match_id, home_team_score: int, away_team_score: int, repo: repository.MatchRepository, session):
    match = repo.get(match_id)  
    match.home_team_score = home_team_score
    match.away_team_score = away_team_score
    session.commit()
    
    return match.id