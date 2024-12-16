import pytest
from src.pybet import schema, services, repository


def test_make_bet():
    match = schema.Match(
        home_team_id=1,
        away_team_id=2
    )    
    bet = schema.Bet(
        user_id = 1,
        match_id = 1,
        home_team_score = 2,
        away_team_score = 3
        
    )
    match.place_bet(bet)
    
    assert len(match.bets)
    assert isinstance(match.bets[0], schema.Bet)
