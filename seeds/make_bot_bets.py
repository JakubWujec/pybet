import sys
import random
from src.pybet import unit_of_work, message_bus, commands, schema

def make_bot_bets(round: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        matches = uow.matches.get_gameround_matches(round)
        bots = uow.session.query(schema.User).filter_by(role=schema.Role.BOT).all()

        for match in matches:
            for bot in bots: 
                message_bus.handle(
                    commands.MakeBetCommand(
                        user_id=bot.id,
                        match_id=match.id,
                        home_team_score=random.randint(0, 5),
                        away_team_score=random.randint(0, 5)
                    ), 
                    uow
                )

if __name__ == "__main__":  
    if len(sys.argv) < 2:
        print("Provide gameround")
    else:
        p1 = sys.argv[1]  
        make_bot_bets(int(p1))
            