from dataclasses import dataclass
from typing import Optional

class Bet:
    match_id: int
    home_team_score: int
    away_team_score: int
    user_id: int
    
    def __init__(self,  user_id: int, match_id: int, home_team_score: int, away_team_score: int):
        self.match_id = match_id
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.user_id = user_id
    
    def __eq__(self, other):
        if not isinstance(other, Bet):
            return NotImplemented
        return (
            self.match_id == other.match_id and
            self.home_team_score == other.home_team_score and
            self.away_team_score == other.away_team_score and
            self.user_id == self.user_id
        )

    def __hash__(self):
        return hash((self.match_id, self.home_team_score, self.away_team_score, self.user_id))
    
    def __repr__(self):
        return f"Bet(match_id={self.match_id}, home_team_score={self.home_team_score}, away_team_score={self.away_team_score}, user_id={self.user_id})"

class Match:
    id: int
    home_team_id: int
    away_team_id: int
    home_team_score: Optional[int] = None 
    away_team_score: Optional[int] = None
    user_bet: Optional[Bet] = None
    
    def __init__(self, home_team_id, away_team_id):
        self.id = None
        self.home_team_score = None
        self.away_team_score = None
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.user_bet = None
    
    