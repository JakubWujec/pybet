from datetime import datetime
from seeds.score_provider import run_score_provider, FPLScoreProvider
from seeds.make_bot_bets import make_bot_bets
from pybet import unit_of_work
from pybet.queries.gamestage_queries import get_gamestage_id_by_date

if __name__ == "__main__":
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    fpl_score_provider = FPLScoreProvider()
    active_gamestage_id = get_gamestage_id_by_date(date=datetime.now(), uow=uow)

    if active_gamestage_id is not None:
        print(f"CURRENT GAMESTAGE ID: {active_gamestage_id}")
        run_score_provider(fpl_score_provider, active_gamestage_id)
        make_bot_bets(active_gamestage_id + 1)
