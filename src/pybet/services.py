from src.pybet import schema, unit_of_work

def make_bet(user_id: int, match_id: int, home_team_score: int, away_team_score: int, uow: unit_of_work.UnitOfWork):
    with uow:
        match = uow.matches.get(match_id)    
        bet = schema.Bet(
            user_id=user_id,
            home_team_score=home_team_score,
            away_team_score=away_team_score
        )    
        match.place_bet(bet)
        uow.commit()
    
        return match.id


def update_match_score(match_id: int, home_team_score: int, away_team_score: int, uow: unit_of_work.UnitOfWork):
    with uow:
        match = uow.matches.get(match_id)  
        match.home_team_score = home_team_score
        match.away_team_score = away_team_score
        uow.commit()
    
        return match.id