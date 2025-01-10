from src.flasky.standings import bp
from src.pybet import unit_of_work, queries
from flask import render_template, request, url_for


@bp.route("/standings", methods=["GET"])
def standings_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    data = queries.standings_query(
        round=2,
        page=page,
        per_page=per_page,
        uow=uow
    )
    standings, count = data['standings'], data['count']
    pagination = paginate("standings.standings_view", page, per_page, count)
    
    return render_template(
        'standings.html',
        standings=standings,
        count=count,
        next_url=pagination['next_url'],
        prev_url=pagination['prev_url']
    )
    
    
def paginate(endpoint, page, per_page, total_count):
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
        "next_url": url_for(endpoint=endpoint, page=next_page) if has_next else None,
        "prev_url": url_for(endpoint=endpoint, page=prev_page) if has_prev else None
    }
    
