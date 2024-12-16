from src.pybet import services
from src.pybet import repository, schema

class FakeSession:
    committed = False

    def commit(self):
        self.committed = True

def test_make_bet_service():
    repo = repository.FakeMatchRepository()
    repo.add(schema.Match(
        home_team_id=2,
        away_team_id=3
    ))
    
    services.make_bet(
        user_id=1,
        match_id=1,
        home_team_score= 1,
        away_team_score= 1,
        repo=repo,
        session=FakeSession()
    )
    
    match = repo.get(1)
    
    assert match.bets
    assert isinstance(match.bets[0], schema.Bet) 