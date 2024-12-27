from src.pybet.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy.sql import text
from datetime import datetime

def mybets(user_id: int, uow: SqlAlchemyUnitOfWork):
    with uow:
        rows = list(uow.session.execute(text(
            'SELECT m.id, ht.id, ht.name, at.id, at.name, m.home_team_score, m.away_team_score, kickoff, b.id, b.home_team_score, b.away_team_score, b.points'
            ' FROM matches AS m'
            ' JOIN teams as ht ON ht.id = m.home_team_id'
            ' JOIN teams as at ON at.id = m.away_team_id'
            ' LEFT JOIN bets AS b on b.match_id = m.id AND b.user_id = :user_id'),
            dict(user_id=user_id)
        ))
    result = []
    for (match_id, home_team_id, home_team_name, away_team_id, away_team_name, home_team_score, away_team_score, kickoff, bet_id, bet_home, bet_away, bet_points) in rows:

        match = {
            "id":match_id,
            "user_id": user_id,
            "home_team_id":home_team_id,
            "away_team_id":away_team_id,
            "home_team": {
                "id": home_team_id,
                "name": home_team_name
            },
            "away_team": {
                "id": away_team_id,
                "name": away_team_name
            },
            "kickoff": kickoff_to_datetime(kickoff),
            "home_team_score": home_team_score,
            "away_team_score": away_team_score,
            "bet": None
        }
        if bet_id is not None:
            match["bet"] = {
                "id": bet_id,
                "home_team_score": bet_home,
                "away_team_score": bet_away,
                "points": bet_points,
            }
        result.append(match)
    
    return result
    
    
def kickoff_to_datetime(kickoff):
    if isinstance(kickoff, datetime):
        return kickoff
    return datetime.strptime(kickoff, "%Y-%m-%d %H:%M:%S.%f")
        