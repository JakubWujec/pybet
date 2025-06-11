from flask import render_template, request
from flask_login import current_user, login_required

from flasky.mygamestage import bp, forms
from pybet import unit_of_work, queries


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
            bet = getattr(match, "bet", dict())
            form.bets.append_entry(
                {
                    "match_id": int(match["id"]),
                    "home_team_score": bet.get("home_team_score", 0),
                    "away_team_score": bet.get("away_team_score", 0),
                }
            )

    return render_template(
        "mygamestage/mygamestage.html",
        gameround_name=gamestage["name"],
        form=form,
        match_by_id=match_by_id,
        current_user=current_user,
        enumerate=enumerate,
    )
