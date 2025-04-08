import datetime

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flasky.points import bp
from pybet import queries, schema, unit_of_work


@bp.route("/points", methods=["GET"])
@login_required
def points():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = current_user.id
    active_gameround = queries.get_active_gameround_by_date(
        datetime.datetime.now(), uow
    )

    if active_gameround is None:
        flash("There is no data to show yet!")
        return redirect(url_for("my-bet.mybets_view"))

    return redirect(
        url_for(
            "points.user_round_points_view", user_id=user_id, round=active_gameround
        )
    )


@bp.route("/points/<user_id>/rounds/<round>", methods=["GET"])
def user_round_points_view(user_id: int, round: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    round = int(round)
    user_id = int(user_id)
    active_gameround = queries.get_active_gameround_by_date(
        datetime.datetime.now(), uow
    )

    # dont allow to lookup future bets of other players
    if round > active_gameround:
        if current_user.is_anonymous or current_user.id != user_id:
            abort(403)

    with uow:
        user: schema.User = uow.session.query(schema.User).get(user_id)
        if user is None:
            abort(404)
        username = user.username

    query_result = queries.mybets(user_id, gameround=round, uow=uow)
    matches = query_result["matches"]

    return render_template(
        "points/entry.html",
        enumerate=enumerate,
        matches=matches,
        gameround=round,
        username=username,
    )
