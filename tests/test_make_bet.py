import pytest
from src.pybet import model, services, repository


def test_make_bet():
    match = model.Match(1, 2)    
    match.place_bet(1, 2, 3)
    
    assert len(match.bets)
    assert isinstance(match.bets[0], model.Bet)
