from src.pybet import services
from src.pybet import repository, model

class FakeSession:
    committed = False

    def commit(self):
        self.committed = True

def test_make_bet_service():
    repo = repository.FakeMatchRepository()
    repo.add(model.Match(2, 3))
    
    services.make_bet(
        user_id=1,
        match_id=1,
        home_team_score= 1,
        away_team_score= 1,
        repo=repo,
        session=FakeSession()
    )
    
    match = repo.get(1)
    
    assert match.user_bet is not None
    assert isinstance(match.user_bet, model.Bet) 