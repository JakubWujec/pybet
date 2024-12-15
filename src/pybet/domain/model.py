from dataclasses import dataclass

@dataclass
class Bet:
    home_team_score: int
    away_team_score: int
    
class Match:
    home_team_id: int
    away_team_id: int
    home_team_score: int
    away_team_score: int