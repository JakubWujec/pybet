from src.pybet import schema
from sqlalchemy.orm import Session
from datetime import datetime
from src import config
import requests

def seed_teams_and_matches_from_fpl(session: Session):
    URL1 = "https://fantasy.premierleague.com/api/bootstrap-static/"
    URL2 = "https://fantasy.premierleague.com/api/fixtures/"
    fpl_teams = {}
    
    r = requests.get(url = URL1)
    data = r.json()
    teams_data = data['teams']
    for row in teams_data:
        short_name = row['short_name']
        team = schema.Team(name = short_name)
        session.add(team)
        fpl_teams[row['id']] = team

    session.flush()   
    
    print(fpl_teams)
    print(list(fpl_teams.keys()))
    
    r = requests.get(url = URL2)
    fixtures_data = r.json()
    for idx, fixture in enumerate(fixtures_data):
        if not fixture['finished'] and fixture['event'] is not None:
            print(f"{idx} {fixture}")
            team_a = fpl_teams[fixture["team_a"]]
            team_h = fpl_teams[fixture["team_h"]]
            match = schema.Match(
                home_team_id = team_h.id,
                away_team_id = team_a.id,
                kickoff = datetime.fromisoformat(fixture["kickoff_time"]),
                gameround=fixture['event']
            )
            session.add(match)

    session.commit()
    
    
if __name__ == "__main__":    
    with config.session_scope() as session:
        seed_teams_and_matches_from_fpl(session)
        
