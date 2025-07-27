import datetime

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from flasky.points import bp
from pybet import unit_of_work
from pybet.queries import bet_queries, queries, match_queries, gamestage_queries


@bp.route("/points", methods=["GET"])
@login_required
def points():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = current_user.id
    previous_gamestage_id = gamestage_queries.get_previous_gamestage_id(uow)

    if previous_gamestage_id is None:
        return render_template("points/before_first_round_finished.html")

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
    all_gamestagesDTO = gamestage_queries.get_all(uow=uow)
    gamestageDTO = next((g for g in all_gamestagesDTO if g.id == gamestage_id), None)

    if gamestageDTO is None:
        abort(404)

    if not can_view_gamestage(
        gamestageDTO=gamestageDTO, viewer_id=user_id, current_user_id=current_user_id
    ):
        abort(403)

    username = queries.get_username_by_user_id(user_id=user_id, uow=uow)
    if username is None:
        abort(404, "User doesn't exist")

    matches = match_queries.get_by_gamestage_id(gamestage_id=gamestage_id, uow=uow)

    betDTOs = bet_queries.get_user_gamestage_bets(
        user_id, gamestage_id=gamestage_id, uow=uow
    )
    betDTO_by_match_id = {bet.match_id: bet for bet in betDTOs}

    prev_gamestageDTO, next_gamestageDTO = get_adjacent_gamestages(
        gamestageDTO, all_gamestagesDTO
    )

    return render_template(
        "points/entry.html",
        enumerate=enumerate,
        matches=matches,
        betDTO_by_match_id=betDTO_by_match_id,
        gamestage_name=gamestageDTO.name,
        username=username,
        next_url=build_gamestage_url(next_gamestageDTO, user_id, current_user_id),
        prev_url=build_gamestage_url(prev_gamestageDTO, user_id, current_user_id),
    )


def can_view_gamestage(
    gamestageDTO: gamestage_queries.GamestageDTO,
    viewer_id,
    current_user_id: int | None,
):
    if gamestageDTO.deadline > datetime.datetime.now():
        return viewer_id == current_user_id
    return True


def get_adjacent_gamestages(current, all_stages):
    try:
        idx = all_stages.index(current)
    except ValueError:
        return None, None

    prev_stage = all_stages[idx - 1] if idx - 1 >= 0 else None
    next_stage = all_stages[idx + 1] if idx + 1 < len(all_stages) else None
    return prev_stage, next_stage


def build_gamestage_url(
    gamestageDTO: gamestage_queries.GamestageDTO | None, user_id, current_user_id
):
    if gamestageDTO is None:
        return None
    if not can_view_gamestage(gamestageDTO, user_id, current_user_id):
        return None
    return url_for(
        "points.user_round_points_view", user_id=user_id, gamestage_id=gamestageDTO.id
    )
