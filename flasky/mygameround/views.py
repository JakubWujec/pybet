from flask import render_template
from flask_login import current_user, login_required

from flasky.mygameround import bp
from pybet import unit_of_work, queries


@bp.route("/mygameround", methods=["GET", "POST"])
@login_required
def mygameround_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    gamestage = queries.get_current_gamestage(uow=uow)

    if gamestage is None:
        return "Gamestage not found"

    return render_template(
        "mygameround/mygameround.html",
        gameround_name=gamestage["name"],
        current_user=current_user,
        enumerate=enumerate,
    )
