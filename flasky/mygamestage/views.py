from flask import abort, flash, redirect, render_template, request
from flask_login import current_user, login_required

from flasky.mygamestage import bp, forms
from pybet import commands, message_bus, unit_of_work
from pybet.queries import gamestage_queries, queries, bet_queries, match_queries


@bp.route("/mygamestage", methods=["GET", "POST"])
@login_required
def mygamestage_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    current_gamestage_DTO = gamestage_queries.get_current_gamestage(uow=uow)
    if current_gamestage_DTO is None:
        abort(404)

    matches = match_queries.get_by_gamestage_id(
        gamestage_id=current_gamestage_DTO.id, uow=uow
    )
    match_by_id = {matchDTO.id: matchDTO for matchDTO in matches}

    bets = bet_queries.get_user_gamestage_bets(
        current_user.id, gamestage_id=current_gamestage_DTO.id, uow=uow
    )
    bet_by_match_id = {bet.match_id: bet for bet in bets}

    form = forms.MatchBetListForm()

    if request.method == "GET":
        for matchDTO in matches:
            bet = bet_by_match_id.get(matchDTO.id, None)
            form.bets.append_entry(
                {
                    "match_id": matchDTO.id,
                    "home_team_score": getattr(bet, "home_team_score", None),
                    "away_team_score": getattr(bet, "away_team_score", None),
                }
            )
    elif request.method == "POST":
        try:
            if form.validate_on_submit():
                gamestage_bets = [
                    commands.GamestageBet(
                        match_id=bet["match_id"],
                        home_team_score=bet["home_team_score"],
                        away_team_score=bet["away_team_score"],
                    )
                    for bet in form.data["bets"]
                ]
                message = commands.MakeGamestageBetCommand(
                    user_id=current_user.id,
                    gamestage_id=current_gamestage_DTO.id,
                    bets=gamestage_bets,
                )

                with uow:
                    message_bus.handle(message, uow)
                    flash("Record was successfully save.", category="success")
            else:
                flash(
                    "Something went wrong. Validate your input and try again.",
                    category="danger",
                )
        except Exception as ex:
            flash(f"Error {ex}", "error")
        finally:
            redirect(request.url)

    return render_template(
        "mygamestage/mygamestage.html",
        gamestageDTO=current_gamestage_DTO,
        form=form,
        match_by_id=match_by_id,
        enumerate=enumerate,
    )
