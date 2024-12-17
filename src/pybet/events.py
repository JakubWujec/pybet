from dataclasses import dataclass

class Event:
    pass 

@dataclass
class MatchScoreUpdated:
    match_id: int
