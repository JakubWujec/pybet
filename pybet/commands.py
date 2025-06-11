from dataclasses import dataclass
from datetime import datetime
from typing import List


class Command:
    pass


@dataclass
class CreateGamestageCommand(Command):
    name: str


@dataclass
class CreateMatchCommand(Command):
    home_team_id: int
    away_team_id: int
    gameround: int
    kickoff: datetime


@dataclass
class GamestageBet:
    match_id: int
    home_team_score: int
    away_team_score: int


@dataclass
class MakeGamestageBetCommand(Command):
    user_id: int
    gamestage_id: int
    bets: List[GamestageBet]


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
