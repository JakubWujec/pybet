import pytest
from src.pybet.domain import model
from src.pybet import services
from src.pybet.repository import FakeMatchRepository

@pytest.fixture()
def fake_match_repo():
    repo = FakeMatchRepository()
    repo.add(
        model.Match(1, 2)
    )
    return repo

def test_make_bet(fake_match_repo):
    bet = services.make_bet(1, 2, 3, fake_match_repo)
    
    assert bet is not None
    assert isinstance(bet, model.Bet)


