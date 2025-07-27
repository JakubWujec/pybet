from datetime import datetime

from flask import abort, redirect, render_template, request, url_for

from flasky.generic.pagination import Pagination
from flasky.standings import bp
from pybet import unit_of_work
from pybet.queries import gamestage_queries, queries

PER_PAGE = 20


@bp.route("/standings", methods=["POST"])
def standings_view_post():
    gamestage_id = request.form.get("gamestage_id", type=int)
    return redirect(url_for("standings.standings_view", gamestage_id=gamestage_id))


@bp.route("/standings", methods=["GET"])
def standings_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    current_gamestage_id = gamestage_queries.get_gamestage_id_by_date(
        datetime.now(), uow=uow
    )

    if current_gamestage_id is None:
        return render_template("standings/before_game_start.html")

    selected_gamestage_id = request.args.get(
        "gamestage_id", current_gamestage_id, type=int
    )
    page = request.args.get("page", 1, type=int)

    available_gamestage_ids = gamestage_queries.get_available_gamestage_ids(uow=uow)
    data = queries.standings_query(
        gamestage_id=selected_gamestage_id,
        page=page,
        per_page=PER_PAGE,
        uow=uow,
    )
    standings, count = data.standings, data.count
    pagination = Pagination(page=page, per_page=PER_PAGE, total=count)
    prev_url, next_url = build_pagination_urls(
        endpoint="standings.standings_view",
        gamestage_id=selected_gamestage_id,
        pagination=pagination,
    )

    return render_template(
        "standings/standings.html",
        available_gamestage_ids=available_gamestage_ids,
        current_gamestage_id=current_gamestage_id,
        selected_gamestage_id=selected_gamestage_id,
        standings=standings,
        count=count,
        next_url=next_url,
        prev_url=prev_url,
    )


def build_pagination_urls(endpoint, gamestage_id, pagination: Pagination):
    return (
        url_for(endpoint, gamestage_id=gamestage_id, page=pagination.next_page)
        if pagination.has_next
        else None,
        url_for(endpoint, gamestage_id=gamestage_id, page=pagination.prev_page)
        if pagination.has_prev
        else None,
    )
