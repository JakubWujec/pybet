from src.flasky.main import bp
from src.pybet import schema, unit_of_work
from src.pybet import message_bus, commands
from src.pybet import queries
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
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
    
    return redirect(f'/entry/{user_id}/rounds/{active_gameround}')

@bp.route("/")
@bp.route("/index")
def index():
    user = current_user
    username = None
    if not current_user.is_anonymous:
        username = user.username
    return render_template('index.html', title='Home', username=username )
