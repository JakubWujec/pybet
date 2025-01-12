from src.pybet.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy.sql import text
from datetime import datetime
from typing import List

def mybets(user_id: int, gameround: int, uow: SqlAlchemyUnitOfWork):
    with uow:
        rows = list(uow.session.execute(text(
            'SELECT m.id, ht.id, ht.name, at.id, at.name, m.home_team_score, m.away_team_score, kickoff, b.id, b.home_team_score, b.away_team_score, b.points'
            ' FROM matches AS m'
            ' JOIN teams as ht ON ht.id = m.home_team_id'
            ' JOIN teams as at ON at.id = m.away_team_id'
            ' LEFT JOIN bets AS b on b.match_id = m.id AND b.user_id = :user_id'
            ' WHERE m.gameround = :gameround'
            ),
            dict(user_id=user_id, gameround=gameround)
        ))
    result = {
        "matches": []
    }
    
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
        result["matches"].append(match)
    
    return result
    
    
def kickoff_to_datetime(kickoff):
    if isinstance(kickoff, datetime):
        return kickoff
    return datetime.strptime(kickoff, "%Y-%m-%d %H:%M:%S.%f")

def get_active_gameround_by_date(current_timestamp: datetime, uow: SqlAlchemyUnitOfWork):
    with uow:
        result = uow.session.execute(text(
            'SELECT MAX(gameround) as gameround'
            ' FROM matches AS m'
            ' WHERE kickoff <= :current_timestamp'
            ), dict(current_timestamp=current_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"))
        ).scalar()
        return result

def get_next_gameround(uow: SqlAlchemyUnitOfWork) -> int | None:
    with uow:
        result = uow.session.execute(text(
            'SELECT MIN(gameround) as gameround'
            ' FROM matches'
            ' WHERE gameround NOT IN'
            ' (SELECT DISTINCT gameround'
            ' FROM matches'
            ' where kickoff <= CURRENT_TIMESTAMP)'
        )).scalar()
        return result
    
def get_available_gamerounds(uow: SqlAlchemyUnitOfWork) -> List[int]:
    with uow:
        result = uow.session.execute(text(
            """
                SELECT DISTINCT gameround FROM matches ORDER BY gameround
            """
        )).all()
        return [row[0] for row in result]

def standings_query(round: int, page:int, per_page:int, uow: SqlAlchemyUnitOfWork):
    offset = (page - 1) * per_page
    with uow:
        count = uow.session.execute(text(
            '''
                SELECT COUNT(DISTINCT u.id)
                FROM users as u
                JOIN bets as b on b.user_id = u.id
                JOIN matches as m on m.id = b.match_id
                WHERE m.gameround = :round
            '''
        ), dict(round=round)).scalar()
        
        rows = uow.session.execute(text(
            '''
                SELECT u.id id, u.username username, SUM(b.points) points, RANK() OVER(ORDER BY b.points) position
                FROM users as u
                JOIN bets as b on b.user_id = u.id
                JOIN matches as m on m.id = b.match_id
                WHERE m.gameround = :round
                GROUP BY u.id, u.username
                LIMIT :limit OFFSET :offset;
            '''
        ), dict(round=round, limit=per_page, offset=offset)).all()
            
    standings = list(map(
        lambda row: {
            "user_id": row[0],
            "username": row[1],
            "points": row[2],
            "position": row[3]  
        }, 
        rows
    ))
    
    return {
        "standings": standings,
        "count": count,
    }
    
    
def get_team_id_by_name(team_name: int, uow: SqlAlchemyUnitOfWork):
    with uow:
        team_id = uow.session.execute(text(
            '''
                SELECT id
                FROM teams
                WHERE name=:team_name
            '''
        ), dict(team_name=team_name)).first()
        return team_id[0]
    
def find_match_id(gameround:int, home_team_id: int, away_team_id: int, uow: SqlAlchemyUnitOfWork):
    with uow:
        match_id = uow.session.execute(text(
            '''
                SELECT id
                FROM matches
                WHERE gameround = :gameround AND home_team_id = :home_team_id AND away_team_id = :away_team_id
            '''
        ), dict(gameround=gameround, home_team_id=home_team_id, away_team_id=away_team_id)).first()
        
        if match_id is None:
            return None
        
        return match_id[0]
    
    