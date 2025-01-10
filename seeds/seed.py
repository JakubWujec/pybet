from src.config import get_session
from src.pybet import schema
from src import config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import datetime
import requests

def seed_teams_and_matches(session):
    future_date = datetime.datetime.now() + datetime.timedelta(days=3)
    past_date = datetime.datetime.now() - datetime.timedelta(days=7)
    team_names = [
        "ARS", "LIV", "CHE", "NOT", "BOU", "AVC", "MCI", "NEW", "FUL", "BRI",
        "TOT", "BRE", "MUN", "WHU", "EVE", "CRY", "LEI", "WOL", "IPS", "SOU"
    ]
    team_dict = {}
    for name in team_names:
        try:
            team = schema.Team(name=name)
            session.add(team)
            team_dict[name] = team
        except IntegrityError:
            pass
    session.flush()
    
    past_matches = [
        schema.Match(home_team_id = team_dict["MCI"].id, away_team_id=team_dict["EVE"].id, kickoff=past_date, gameround=1),
        schema.Match(home_team_id = team_dict["BOU"].id, away_team_id=team_dict["CRY"].id, kickoff=past_date, gameround=1),
        schema.Match(home_team_id = team_dict["CHE"].id, away_team_id=team_dict["FUL"].id, kickoff=past_date, gameround=1),
        schema.Match(home_team_id = team_dict["NEW"].id, away_team_id=team_dict["AVC"].id, kickoff=past_date, gameround=1),
        schema.Match(home_team_id = team_dict["NOT"].id, away_team_id=team_dict["TOT"].id, kickoff=past_date, gameround=1),
    ]
        
    future_matches = [
        schema.Match(home_team_id = team_dict["SOU"].id, away_team_id=team_dict["WHU"].id, kickoff=future_date, gameround=2),
        schema.Match(home_team_id = team_dict["WOL"].id, away_team_id=team_dict["MUN"].id, kickoff=future_date, gameround=2),
        schema.Match(home_team_id = team_dict["LIV"].id, away_team_id=team_dict["LEI"].id, kickoff=future_date, gameround=2),
        schema.Match(home_team_id = team_dict["BRI"].id, away_team_id=team_dict["BRE"].id, kickoff=future_date, gameround=2),
        schema.Match(home_team_id = team_dict["ARS"].id, away_team_id=team_dict["IPS"].id, kickoff=future_date, gameround=2),
    ]
    
    for match in past_matches:
        session.add(match)
        
    for match in future_matches:
        session.add(match)
        
    session.commit()


    
if __name__ == "__main__":    
    with config.session_scope() as session:
        seed_teams_and_matches(session)
        
