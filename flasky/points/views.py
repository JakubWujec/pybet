import datetime

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flasky.points import bp
from pybet import queries, unit_of_work


@bp.route("/points", methods=["GET"])
@login_required
def points():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = current_user.id
    previous_gamestage_id = queries.get_previous_gamestage_id(uow)

    if previous_gamestage_id is None:
        flash("There is no data to show yet!")
        return redirect(url_for("mygamestage.mygamestage_view"))

    return redirect(
        url_for(
            "points.user_round_points_view",
            user_id=user_id,
            gamestage_id=previous_gamestage_id,
        )
    )


@bp.route("/points/<user_id>/gamestage/<gamestage_id>", methods=["GET"])
def user_round_points_view(user_id: int, gamestage_id: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = int(user_id)

    gamestageDTO = queries.get_gamestage_by_id(gamestage_id=gamestage_id, uow=uow)
    print(gamestage_id)
    print(gamestageDTO)
    if gamestageDTO is None:
        abort(404)

    # dont allow to lookup future bets of other players
    if gamestageDTO.deadline > datetime.datetime.now():
        if current_user.is_anonymous or current_user.id != user_id:
            abort(403)

    username = queries.get_username_by_user_id(user_id=user_id, uow=uow)
    if username is None:
        abort(404, "User doesn't exist")

    query_result = queries.mygamestage(user_id, gamestage_id=gamestage_id, uow=uow)
    matches = query_result["matches"]

    return render_template(
        "points/entry.html",
        enumerate=enumerate,
        matches=matches,
        gamestage_name=gamestageDTO.name,
        username=username,
    )
