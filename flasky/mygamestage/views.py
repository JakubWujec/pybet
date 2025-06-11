from flask import render_template
from flask_login import current_user, login_required

from flasky.mygamestage import bp
from pybet import unit_of_work, queries


@bp.route("/mygamestage", methods=["GET", "POST"])
@login_required
def mygamestage_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    gamestage = queries.get_current_gamestage(uow=uow)

    if gamestage is None:
        return "Gamestage not found"

    matches = queries.mygamestage(
        user_id=current_user.id, gamestage_id=gamestage["id"], uow=uow
    )["matches"]

    return render_template(
        "mygamestage/mygamestage.html",
        gameround_name=gamestage["name"],
        current_user=current_user,
        enumerate=enumerate,
    )
