from dataclasses import dataclass

class Event:
    pass 

@dataclass
class MatchScoreUpdated(Event):
    match_id: int
