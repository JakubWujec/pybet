from dataclasses import dataclass
from datetime import datetime
class Command:
    pass 

@dataclass
class CreateMatchCommand(Command):
    home_team_id: int
    away_team_id: int
    gameround: int
    kickoff: datetime

@dataclass
class MakeBetCommand(Command):
    user_id: int
    match_id: int
    home_team_score: int
    away_team_score: int

@dataclass
class UpdateMatchScoreCommand(Command):
    match_id: int
    home_team_score: int
    away_team_score: int    