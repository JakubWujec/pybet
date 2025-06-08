import random
import sys

from pybet import commands, handlers, schema, unit_of_work


def make_bot_bets(round: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        matches = uow.matches.get_gameround_matches(round)
        bots = uow.session.query(schema.User).filter_by(role=schema.Role.BOT).all()

        for match in matches:
            for bot in bots:
                handlers.make_bet(
                    commands.MakeBetCommand(
                        user_id=bot.id,
                        match_id=match.id,
                        home_team_score=random.randint(0, 5),
                        away_team_score=random.randint(0, 5),
                    ),
                    uow,
                    skip_validation=True,
                )


if __name__ == "__main__":
    print("Run Seed: Make bot bets")
    if len(sys.argv) < 2:
        print("Provide gameround")
    else:
        p1 = sys.argv[1]
        make_bot_bets(int(p1))
