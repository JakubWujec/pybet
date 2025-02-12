from pybet import message_bus, commands, unit_of_work
from pybet.score_provider import FPLScoreProvider
from seeds.fpl_data import get_team_code_by_fpl_id
import sys

#>py -m seeds.fpl_update_score

def update_score_from_fpl(round: int):
    score_provider = FPLScoreProvider()
    match_results = score_provider.get_match_results(round)
    
   
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    
    with uow:
        matches = uow.matches.get_gameround_matches(round)
            
        for _match in matches:
            found_result = next((result for result in match_results if result.home_team_short_name == _match.home_team.name and result.away_team_short_name == _match.away_team.name), None)
            if found_result:
                message_bus.handle(
                    commands.UpdateMatchScoreCommand(
                        match_id=_match.id,
                        home_team_score=found_result.home_team_score,
                        away_team_score=found_result.away_team_score
                    ),
                    uow
                )



if __name__ == "__main__":  
    if len(sys.argv) < 2:
        print("Provide gameround")
    else:
        p1 = sys.argv[1]  
        update_score_from_fpl(int(p1))
            