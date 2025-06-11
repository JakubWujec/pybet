from typing import List
from flask import flash, redirect, render_template, request
from flask_login import current_user, login_required

from flasky.mygamestage import bp, forms
from pybet import commands, message_bus, unit_of_work, queries


@bp.route("/mygamestage", methods=["GET", "POST"])
@login_required
def mygamestage_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    gamestage = queries.get_current_gamestage(uow=uow)

    if gamestage is None:
        return "Gamestage not found"

    matches = queries.mygamestage(
        user_id=current_user.id, gamestage_id=gamestage["id"], uow=uow
    )["matches"]
    match_by_id = {match["id"]: match for match in matches}
    form = forms.MatchBetListForm()

    if request.method == "GET":
        for match in matches:
            bet = getattr(match, "bet", match["bet"] or dict())  # TODO FIX TOFIX
            form.bets.append_entry(
                {
                    "match_id": int(match["id"]),
                    "home_team_score": bet.get("home_team_score", 0),
                    "away_team_score": bet.get("away_team_score", 0),
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
                    gamestage_id=gamestage["id"],
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
            redirect(request.url)

    return render_template(
        "mygamestage/mygamestage.html",
        gamestage_name=gamestage["name"],
        form=form,
        match_by_id=match_by_id,
        current_user=current_user,
        enumerate=enumerate,
    )
