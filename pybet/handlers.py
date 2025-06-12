from datetime import datetime, timezone

from pybet import commands, events, schema, services, unit_of_work


class MatchAlreadyStarted(Exception):
    pass


class MatchNotFound(Exception):
    pass


def create_gamestage(
    command: commands.CreateGamestageCommand, uow: unit_of_work.UnitOfWork
):
    with uow:
        gamestage = schema.Gamestage(id=command.id, name=command.name)
        uow.gamestages.add(gamestage)
        uow.commit()


def create_match(command: commands.CreateMatchCommand, uow: unit_of_work.UnitOfWork):
    with uow:
        match = schema.Match(
            home_team_id=command.home_team_id,
            away_team_id=command.away_team_id,
            gamestage_id=command.gamestage_id,
            kickoff=command.kickoff,
        )
        uow.matches.add(
            match=match,
        )
        uow.commit()


def make_gamestage_bet(
    command: commands.MakeGamestageBetCommand, uow: unit_of_work.UnitOfWork
):
    with uow:
        gamestage = uow.gamestages.get(command.gamestage_id)
        print(command)

        for command_bet in command.bets:
            match = uow.matches.get(command_bet.match_id)

            if match is None:
                raise MatchNotFound()

            if match.is_after_kickoff():
                raise MatchAlreadyStarted(
                    f"Now: {datetime.now(timezone.utc)}, kickoff: {match.kickoff}"
                )

            new_bet = schema.Bet(
                user_id=command.user_id,
                home_team_score=command_bet.home_team_score,
                away_team_score=command_bet.away_team_score,
                points=0,
            )
            match.place_bet(new_bet)
            uow.commit()

        return gamestage


def make_bet(
    command: commands.MakeBetCommand,
    uow: unit_of_work.UnitOfWork,
    skip_validation=False,
):
    with uow:
        match = uow.matches.get(command.match_id)

        if match is None:
            raise MatchNotFound()

        if not skip_validation and match.is_after_kickoff():
            raise MatchAlreadyStarted(
                f"Now: {datetime.now(timezone.utc)}, kickoff: {match.kickoff}"
            )

        bet = schema.Bet(
            user_id=command.user_id,
            home_team_score=command.home_team_score,
            away_team_score=command.away_team_score,
            points=0,
        )
        match.place_bet(bet)
        uow.commit()

        return match.id


def update_match_score(
    command: commands.UpdateMatchScoreCommand, uow: unit_of_work.UnitOfWork
):
    with uow:
        match = uow.matches.get(command.match_id)
        match.update_score(
            home_team_score=command.home_team_score,
            away_team_score=command.away_team_score,
        )
        uow.commit()
        return match.id


def update_bet_points_for_match(
    event: events.MatchScoreUpdated, uow: unit_of_work.UnitOfWork
):
    with uow:
        match = uow.matches.get(event.match_id)
        for bet in match.bets.values():
            bet.points = services.calculate_points(
                bet.home_team_score,
                bet.away_team_score,
                match.home_team_score,
                match.away_team_score,
            )
        uow.commit()
