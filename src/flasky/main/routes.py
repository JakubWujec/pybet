from src.flasky.main import bp
from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required


@bp.route("/")
@bp.route("/index")
def index():
    user = current_user
    username = None
    if not current_user.is_anonymous:
        username = user.username
    return render_template('index.html', title='Home', username=username )
