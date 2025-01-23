from datetime import datetime
from seeds.fpl_update_score import update_score_from_fpl
from seeds.make_bot_bets import make_bot_bets
from pybet import unit_of_work
from pybet.queries import get_active_gameround_by_date

if __name__ == "__main__":    
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    current_gameround = get_active_gameround_by_date(current_timestamp=datetime.now(), uow=uow)
    print(f"CURRENT GAMEROUND: {current_gameround}")
    update_score_from_fpl(current_gameround)
    make_bot_bets(current_gameround + 1)
        
     