import requests
from src.pybet import message_bus, commands, queries, unit_of_work, schema
from seeds.fpl_data import get_team_code_by_fpl_id
import sys

#>py -m seeds.fpl_update_score

def update_score_from_fpl(round: int):
    URL = f"https://fantasy.premierleague.com/api/fixtures/?event={round}"
    r = requests.get(url = URL)
    data = r.json()    
    team_id_by_name = {}
    match_id_by_home_team_id = {}
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        team_rows = uow.session.query(schema.Team).all()
        for row in team_rows:
            team_id_by_name[row.name] = row.id
        match_rows = uow.session.query(schema.Match).filter_by(gameround=round).all()
        for row in match_rows:
            match_id_by_home_team_id[row.home_team_id] = row.id


    for fixture in data:
        if fixture['finished']:
            home_team_fpl_id = fixture['team_h']
            away_team_fpl_id = fixture['team_a']
            home_team_code = get_team_code_by_fpl_id(home_team_fpl_id)
            away_team_code = get_team_code_by_fpl_id(away_team_fpl_id)
            home_team_id = team_id_by_name[home_team_code]
            # away_team_id = team_id_by_name[away_team_code]
            home_team_score = fixture['team_h_score']
            away_team_score = fixture['team_a_score']
            match_id = match_id_by_home_team_id[home_team_id]
            
            if match_id:
                message_bus.handle(
                    commands.UpdateMatchScoreCommand(
                        match_id=match_id,
                        home_team_score=home_team_score,
                        away_team_score=away_team_score
                    ),
                    uow
                )



if __name__ == "__main__":  
    if len(sys.argv) < 2:
        print("Provide gameround")
    else:
        p1 = sys.argv[1]  
        update_score_from_fpl(int(p1))
            