import pytest
from src.pybet import model, services, repository


@pytest.fixture()
def fake_match_repo():
    repo = repository.FakeMatchRepository()
    repo.add(
        model.Match(1, 2)
    )
    return repo

def test_make_bet(fake_match_repo):
    bet = services.make_bet(1, 1, 2, 3, fake_match_repo)
    
    assert bet is not None
    assert isinstance(bet, model.Bet)


def test_user_cannot_have_multiple_best_on_the_same_match(fake_match_repo):
    bet = services.make_bet(1, 1, 2, 3, fake_match_repo)
    
    assert bet is not None
    assert isinstance(bet, model.Bet)
    
    bet = services.make_bet(1, 1, 3, 4, fake_match_repo)
