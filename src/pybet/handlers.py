from src.pybet import schema, unit_of_work, commands, events, message_bus

from datetime import datetime, timezone

class MatchAlreadyStarted(Exception):
    pass

class MatchNotFound(Exception):
    pass

def create_match(command: commands.CreateMatchCommand, uow: unit_of_work.UnitOfWork):
    with uow:
        match = schema.Match(
            home_team_id=command.home_team_id,
            away_team_id = command.away_team_id,
            gameround = command.gameround,
            kickoff = command.kickoff
        )
        uow.matches.add(
            match=match,
        )
        uow.commit()

def make_bet(command: commands.MakeBetCommand, uow: unit_of_work.UnitOfWork):
    with uow:
        match = uow.matches.get(command.match_id)    
        
        if match is None:
            raise MatchNotFound()
        
        if match.is_after_kickoff():
            raise MatchAlreadyStarted(f"Now: {datetime.now(timezone.utc)}, kickoff: {match.kickoff}")
        
        bet = schema.Bet(
            user_id=command.user_id,
            home_team_score=command.home_team_score,
            away_team_score=command.away_team_score,
            points = 0
        )    
        match.place_bet(bet)
        uow.commit()
    
        return match.id


def update_match_score(command: commands.UpdateMatchScoreCommand, uow: unit_of_work.UnitOfWork):
    with uow:
        try:
            match = uow.matches.get(command.match_id)  
            match.home_team_score = command.home_team_score
            match.away_team_score = command.away_team_score
            uow.commit()
            
            return match.id
        finally:
            message_bus.handle(
                events.MatchScoreUpdated(match_id=match.id),
                uow
            )
     
def update_bet_points_for_match(event: events.MatchScoreUpdated, uow: unit_of_work.UnitOfWork):
    with uow:
        match = uow.matches.get(event.match_id)
        for bet in match.bets.values():
            bet.points = bet.calculate_points(match.home_team_score, match.away_team_score)            
        uow.commit()