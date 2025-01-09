from src.flasky.standings import bp
from src.pybet import unit_of_work, queries
from flask import render_template


@bp.route("/standings", methods=["GET"])
def standings_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    data = queries.standings_query(
        round=2, uow=uow
    )
    
    
    return render_template(
        'standings.html',
        standings=data['standings']
    )
