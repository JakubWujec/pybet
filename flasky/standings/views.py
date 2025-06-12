from flasky.standings import bp
from pybet import unit_of_work, queries
from flask import render_template, request, url_for, redirect
from datetime import datetime


@bp.route("/standings", methods=["POST"])
def standings_view_post():
    gamestage_id = request.form.get("gamestage_id", type=int)
    print(f"YYY {gamestage_id}")
    return redirect(url_for("standings.standings_view", gamestage_id=gamestage_id))


@bp.route("/standings", methods=["GET"])
def standings_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    current_gamestage_id = queries.get_gamestage_id_by_date(datetime.now(), uow=uow)
    selected_gamestage_id = request.args.get(
        "gamestage_id", current_gamestage_id, type=int
    )
    print(f"XXX {selected_gamestage_id}")
    print(f"XXX {request.args.get('gamestage_id')}")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    available_gamestage_ids = queries.get_available_gamestage_ids(uow=uow)
    data = queries.standings_query(
        gamestage_id=selected_gamestage_id, page=page, per_page=per_page, uow=uow
    )
    standings, count = data["standings"], data["count"]
    pagination = paginate(page, per_page, count)
    next_url = (
        url_for(
            endpoint="standings.standings_view",
            gamestage_id=selected_gamestage_id,
            page=pagination["next_page"],
        )
        if pagination["has_next"]
        else None
    )
    prev_url = (
        url_for(
            endpoint="standings.standings_view",
            gamestage_id=selected_gamestage_id,
            page=pagination["prev_page"],
        )
        if pagination["has_prev"]
        else None
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


def paginate(page, per_page, total_count):
    total_pages = (total_count + per_page - 1) // per_page
    has_next = page < total_pages
    has_prev = page > 1
    next_page = page + 1 if has_next else None
    prev_page = page - 1 if has_prev else None

    return {
        "has_next": has_next,
        "has_prev": has_prev,
        "next_page": next_page,
        "prev_page": prev_page,
        "total_pages": total_pages,
    }
