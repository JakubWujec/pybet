from src.config import get_session
from src.pybet import schema
from sqlalchemy.exc import IntegrityError
import datetime

def seed_db():
    future_date = datetime.datetime.now() + datetime.timedelta(days=3)
    
    session = get_session()
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
        
    matches = [
        schema.Match(home_team_id = team_dict["MCI"].id, away_team_id=team_dict["EVE"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["BOU"].id, away_team_id=team_dict["CRY"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["CHE"].id, away_team_id=team_dict["FUL"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["NEW"].id, away_team_id=team_dict["AVC"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["NOT"].id, away_team_id=team_dict["TOT"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["SOU"].id, away_team_id=team_dict["WHU"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["WOL"].id, away_team_id=team_dict["MUN"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["LIV"].id, away_team_id=team_dict["LEI"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["BRI"].id, away_team_id=team_dict["BRE"].id, kickoff=future_date),
        schema.Match(home_team_id = team_dict["ARS"].id, away_team_id=team_dict["IPS"].id, kickoff=future_date),
    ]
    for match in matches:
        session.add(match)
    session.commit()
    
if __name__ == "__main__":
    seed_db()
