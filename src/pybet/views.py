from src.pybet.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy.sql import text


def mybets(user_id: int, uow: SqlAlchemyUnitOfWork):
    with uow:
        rows = list(uow.session.execute(text(
            'SELECT m.id, home_team_id, away_team_id, m.home_team_score, m.away_team_score, kickoff, b.id, b.home_team_score, b.away_team_score'
            ' FROM matches AS m'
            ' LEFT JOIN bets AS b on b.match_id = m.id'),
            dict(user_id=user_id)
        ))
    result = []
    for (match_id, home_team_id, away_team_id, home_team_score, away_team_score, kickoff, bet_id, bet_home, bet_away) in rows:
        match = {
            "id":match_id,
            "user_id": user_id,
            "home_team_id":home_team_id,
            "away_team_id":away_team_id,
            "kickoff":kickoff,
            "home_team_score": home_team_score,
            "away_team_score": away_team_score,
            "bet": None
        }
        if bet_id is not None:
            match["bet"] = {
                "id": bet_id,
                "home_team_score": bet_home,
                "away_team_score": bet_away
            }
        result.append(match)
    
    return result
    