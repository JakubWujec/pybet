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


@bp.route("/points/<int:user_id>/gamestage/<int:gamestage_id>", methods=["GET"])
def user_round_points_view(user_id: int, gamestage_id: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    current_user_id = getattr(current_user, "id", None)
    gamestageDTO: queries.GamestageDTO = get_gamestageDTO_or_abort(
        gamestage_id=gamestage_id, uow=uow
    )

    if not can_view_gamestage(
        gamestageDTO=gamestageDTO, viewer_id=user_id, current_user_id=current_user_id
    ):
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


def get_gamestageDTO_or_abort(gamestage_id: int, uow):
    try:
        gamestageDTO = queries.get_gamestage_by_id(gamestage_id=gamestage_id, uow=uow)
        if gamestageDTO is None:
            abort(404)
        return gamestageDTO
    except Exception:
        abort(404)


def can_view_gamestage(
    gamestageDTO: queries.GamestageDTO, viewer_id, current_user_id: int | None
):
    if gamestageDTO.deadline > datetime.datetime.now():
        return viewer_id == current_user_id
    return True
