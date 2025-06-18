import os

from flask import (
    render_template,
    send_from_directory,
)
from flask_login import current_user

from flasky.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    user = current_user
    username = None
    if not current_user.is_anonymous:
        username = user.username
    # return render_template('index.html', title='Home', username=username )
    return render_template("index.html", title="Home", username=username)


@bp.route("/favicon.ico")
def favicon():
    print(os.path.join(os.path.dirname(bp.root_path), "static"))
    return send_from_directory(
        os.path.join(os.path.dirname(bp.root_path), "static"),
        "favicon.ico",
    )
