import requests
from src.pybet import message_bus, commands, queries, unit_of_work
from seeds.fpl_data import get_team_code_by_fpl_id
import sys

#>py -m seeds.fpl_update_score

def update_score_from_fpl(round: int):
    URL = f"https://fantasy.premierleague.com/api/fixtures/?event={round}"
    r = requests.get(url = URL)
    data = r.json()    
    
    uow = unit_of_work.SqlAlchemyUnitOfWork()
        
    for fixture in data:
        if fixture['finished']:
            home_team_fpl_id = fixture['team_h']
            away_team_fpl_id = fixture['team_a']
            home_team_code = get_team_code_by_fpl_id(home_team_fpl_id)
            away_team_code = get_team_code_by_fpl_id(away_team_fpl_id)
            home_team_id = queries.get_team_id_by_name(home_team_code, uow)
            away_team_id = queries.get_team_id_by_name(away_team_code, uow)
            home_team_score = fixture['team_h_score']
            away_team_score = fixture['team_a_score']
            match_id = queries.find_match_id(round, home_team_id, away_team_id, uow)
            
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
            