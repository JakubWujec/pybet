from src.pybet import repository, schema, unit_of_work, commands, events, handlers, message_bus
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
  
    history = [
        commands.CreateMatchCommand(home_team_id=2, away_team_id=3, gameround=1, kickoff=tommorow),
        commands.MakeBetCommand(user_id=1, match_id=1, home_team_score=1, away_team_score=1),
    ]
    
    for message in history:
        message_bus.handle(message, uow)
  
    match = uow.matches.get(1)
    
    assert isinstance(match.bets[1], schema.Bet) 
    assert match.bets[1].points == 0 
    
def test_making_bet_for_the_same_user_and_match_doesnt_create_multiple_rows():
    uow = FakeUnitOfWork()

    history = [
        commands.CreateMatchCommand(home_team_id=2, away_team_id=3, gameround=1, kickoff=tommorow),
        commands.MakeBetCommand(user_id=1, match_id=1, home_team_score=1, away_team_score=1),
        commands.MakeBetCommand(user_id=1, match_id=1, home_team_score=1, away_team_score=1),
    ]
    
    for message in history:
        message_bus.handle(message, uow)
   
    
    match = uow.matches.get(1)
    
    assert len(match.bets) == 1
    
def test_making_second_bet_updates_scores():
    uow = FakeUnitOfWork()

    history = [
        commands.CreateMatchCommand(home_team_id=2, away_team_id=3, gameround=1, kickoff=tommorow),
        commands.MakeBetCommand(user_id=1, match_id=1, home_team_score=1, away_team_score=1),
        commands.MakeBetCommand(user_id=1, match_id=1, home_team_score=2, away_team_score=3),
    ]
    
    for message in history:
        message_bus.handle(message, uow)
   
    
    match = uow.matches.get(1)
    bet = match.bets[1]
    assert bet.home_team_score == 2
    assert bet.away_team_score == 3
    
def test_when_two_bets_from_different_user_the_two_rows_inseted():
    uow = FakeUnitOfWork()
    
    history = [
        commands.CreateMatchCommand(home_team_id=2, away_team_id=3, gameround=1, kickoff=tommorow),
        commands.MakeBetCommand(user_id=1, match_id=1, home_team_score=1, away_team_score=1),
        commands.MakeBetCommand(user_id=2, match_id=1, home_team_score=1, away_team_score=1),
    ]
    
    for message in history:
        message_bus.handle(message, uow)
   
    
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
    
    handlers.update_match_score(
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
        
    
    with pytest.raises(handlers.MatchAlreadyStarted):
        handlers.make_bet(
            command,
            uow=uow
        )
        
def test_update_bet_points_service_when_exact_score():
    uow = FakeUnitOfWork()

    HOME_SCORE = 2
    AWAY_SCORE = 3
    
    history = [
        commands.CreateMatchCommand(home_team_id=2, away_team_id=3, gameround=1, kickoff=tommorow),
        commands.MakeBetCommand(user_id=1, match_id=1, home_team_score=HOME_SCORE, away_team_score=AWAY_SCORE),
        commands.UpdateMatchScoreCommand(match_id=1, home_team_score=HOME_SCORE, away_team_score=AWAY_SCORE)
    ]
    
    for cmd in history:
        message_bus.handle(cmd, uow)
        
    updated_score_event = events.MatchScoreUpdated(
        match_id = 1
    )
    
    handlers.update_bet_points_for_match(updated_score_event, uow)
    match = uow.matches.get(1)
    
    assert match.bets[1].points == 5
