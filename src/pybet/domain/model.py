from dataclasses import dataclass
from typing import Optional

@dataclass
class Bet:
    match_id: int
    home_team_score: int
    away_team_score: int
    

class Match:
    id: int
    home_team_id: int
    away_team_id: int
    home_team_score: Optional[int] = None 
    away_team_score: Optional[int] = None
    
    def __init__(self, home_team_id, away_team_id):
        self.id = None
        self.home_team_score = None
        self.away_team_score = None
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
    
    