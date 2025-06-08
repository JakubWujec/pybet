from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flasky.mybet import bp, forms
from pybet import commands, message_bus, queries, unit_of_work
from pybet.handlers import MatchAlreadyStarted


@bp.route("/my-bets", methods=["GET", "POST"])
@login_required
def mybets_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    next_gameround = queries.get_next_gameround(uow=uow)
    query_result = queries.mybets(
        user_id=current_user.id, gameround=next_gameround, uow=uow
    )
    matches = query_result["matches"]
    match_by_id = {match["id"]: match for match in matches}
    form = forms.MatchBetListForm()

    if request.method == "GET":
        if next_gameround is None:
            return render_template(
                "mybet/end_of_season.html",
                standings_url=url_for("standings.standings_view"),
            )

        for match in matches:
            bet = getattr(match, "bet", dict())
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
                cmds = [
                    commands.MakeBetCommand(
                        user_id=current_user.id,
                        match_id=bet["match_id"],
                        home_team_score=bet["home_team_score"],
                        away_team_score=bet["away_team_score"],
                    )
                    for bet in form.data["bets"]
                ]

                with uow:
                    for message in cmds:
                        message_bus.handle(message, uow)
                flash("Record was successfully save.", category="success")
            else:
                flash(
                    "Something went wrong. Validate your input and try again.",
                    category="danger",
                )
        except MatchAlreadyStarted as ex:
            flash("Too late. Some matches already started", "error")
            redirect(request.url)

    return render_template(
        "mybet/mybet.html",
        current_user=current_user,
        match_by_id=match_by_id,
        enumerate=enumerate,
        form=form,
        gameround=next_gameround,
    )
