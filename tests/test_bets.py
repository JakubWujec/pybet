from src.pybet.domain import model
from src.pybet import services

def test_make_bet():
    bet = services.make_bet(1, 2, 3)
    
    assert bet is not None
    assert isinstance(bet, model.Bet)


