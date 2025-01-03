from src.flasky.entry import bp
from flask_login import login_user, logout_user, current_user
from flask import request, render_template
from src.pybet import unit_of_work, queries
import datetime

@bp.route("/entry/<user_id>/rounds/<round>", methods=["GET"])
def user_round_entry_view(user_id: int, round: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    matches = queries.mybets(user_id, uow)

    return render_template(
        'entry.html',
        enumerate=enumerate,
        matches=matches
    )
    
