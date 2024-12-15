import pytest
from src.pybet import model, services, repository


def test_make_bet():
    match = model.Match(1, 2)    
    match.place_bet(1, 2, 3)
    
    assert match.user_bet is not None
    assert isinstance(match.user_bet, model.Bet)
