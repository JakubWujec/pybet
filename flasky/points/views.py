from flasky.points import bp
from flask_login import login_user, logout_user, current_user, login_required
from flask import request, render_template, flash, url_for, redirect, abort
from pybet import unit_of_work, queries, schema
import datetime

@bp.route('/points', methods=['GET'])
@login_required
def points():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = current_user.id
    active_gameround = queries.get_active_gameround_by_date(datetime.datetime.now(), uow)
    
    if active_gameround is None:
        flash("There is no data to show yet!")
        return redirect(url_for('my-bet.mybets_view'))
    
    return redirect(url_for("points.user_round_points_view", user_id=user_id, round=active_gameround))


@bp.route("/points/<user_id>/rounds/<round>", methods=["GET"])
def user_round_points_view(user_id: int, round: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    round = int(round)
    user_id = int(user_id)
    active_gameround = queries.get_active_gameround_by_date(datetime.datetime.now(), uow)
    
    if current_user.id != user_id and round > active_gameround:
        return redirect(url_for("points.user_round_points_view", user_id=user_id, round=active_gameround))
    
    with uow:
        user: schema.User = uow.session.query(schema.User).get(user_id)
        if user is None: 
            abort(404)
        username = user.username
   
    query_result = queries.mybets(user_id, gameround=round, uow=uow)
    matches = query_result["matches"]
    
    return render_template(
        'points/entry.html',
        enumerate=enumerate,
        matches=matches,
        gameround=round,
        username=username
    )
    
