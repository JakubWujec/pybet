from datetime import datetime
from seeds.fpl_update_score import update_score_from_fpl
from seeds.make_bot_bets import make_bot_bets
from pybet import unit_of_work
from pybet.queries import get_gamestage_id_by_date

if __name__ == "__main__":
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    active_gamestage_id = get_gamestage_id_by_date(date=datetime.now(), uow=uow)

    if active_gamestage_id is not None:
        print(f"CURRENT GAMESTAGE ID: {active_gamestage_id}")
        update_score_from_fpl(active_gamestage_id)
        make_bot_bets(active_gamestage_id + 1)
