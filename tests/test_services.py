from src.pybet import services
from src.pybet import repository, schema, unit_of_work, commands
import pytest
import datetime 

yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
tommorow = datetime.datetime.now() + datetime.timedelta(days=1)

class FakeSession:
    committed = False

    def commit(self):
        self.committed = True
        
class FakeUnitOfWork(unit_of_work.UnitOfWork):
    def __init__(self):
        self.matches = repository.FakeMatchRepository()
        self.committed = False
    
    def commit(self):
        self.committed = True

    def rollback(self):
        pass

def test_make_bet_service():
    uow = FakeUnitOfWork()
  
    uow.matches.add(schema.Match(
        home_team_id=2,
        away_team_id=3,
        kickoff = tommorow
    ))
    
    command = commands.MakeBetCommand(
        user_id=1,
        match_id=1,
        home_team_score= 1,
        away_team_score= 1,
    )
    
    services.make_bet(
        command,
        uow=uow
    )
    
    match = uow.matches.get(1)
    
    assert isinstance(match.bets[1], schema.Bet) 
    
def test_making_bet_for_the_same_user_and_match_doesnt_create_multiple_rows():
    uow = FakeUnitOfWork()

    uow.matches.add(schema.Match(
        home_team_id=2,
        away_team_id=3,
        kickoff = tommorow
    ))
    
    command1 = commands.MakeBetCommand(
        user_id=1,
        match_id=1,
        home_team_score= 1,
        away_team_score= 1,
    )
    
    services.make_bet(
        command1,
        uow=uow
    )
    
    services.make_bet(
        command1,
        uow=uow
    )
    
    match = uow.matches.get(1)
    
    assert len(match.bets) == 1
    
def test_when_two_bets_from_different_user_the_two_rows_inseted():
    uow = FakeUnitOfWork()
    uow.matches.add(schema.Match(
        home_team_id=2,
        away_team_id=3,
        kickoff = tommorow
    ))
    
    command1 = commands.MakeBetCommand(
        user_id=1,
        match_id=1,
        home_team_score= 1,
        away_team_score= 1,
    )
    
    command2 = commands.MakeBetCommand(
        user_id=2,
        match_id=1,
        home_team_score= 1,
        away_team_score= 1,
    )
    
    
    services.make_bet(
        command1,
        uow=uow
    )
    
    services.make_bet(
        command2,
        uow=uow
    )
    
    match = uow.matches.get(1)
    
    assert len(match.bets) == 2
    
def test_update_match_score_service():
    uow = FakeUnitOfWork()
    uow.matches.add(schema.Match(
        home_team_id=2,
        away_team_id=3
    ))
    
    command = commands.UpdateMatchScoreCommand(
        match_id=1,
        home_team_score= 5,
        away_team_score= 5
    )
    
    services.update_match_score(
        command,
        uow=uow
    )
    
    match = uow.matches.get(1)
    
    assert match.home_team_score == 5
    assert match.away_team_score == 5
    
    
def test_make_bet_error_for_started_match():
    uow = FakeUnitOfWork()

    with uow:
        uow.matches.add(schema.Match(
            home_team_id=2,
            away_team_id=3,
            kickoff = yesterday
        ))
        
    command = commands.MakeBetCommand(
        user_id=1,
        match_id=1,
        home_team_score= 1,
        away_team_score= 1,
    )
        
    
    with pytest.raises(services.MatchAlreadyStarted):
        services.make_bet(
            command,
            uow=uow
        )