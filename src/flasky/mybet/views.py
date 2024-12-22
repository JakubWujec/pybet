from src.flasky.mybet import bp
from src.pybet import schema, unit_of_work, queries
from src.pybet import message_bus, commands
from flask import request, render_template, flash, redirect
from src.flasky.forms.bet_form import BetForm
from src.flasky.forms.match_form import MatchForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime
from src.config import get_session


@bp.route("/my-bets", methods=["GET", "POST"])
@login_required
def mybets_view():
    if request.method == "GET":
    
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        matches = queries.mybets(current_user.id, uow)

        return render_template(
            'mybet.html',
            current_user=current_user,
            matches=matches,
            enumerate=enumerate
        )
    else:
        print(f"FORM: {request.form}")
        print(f"LIST {request.form.getlist("bets")}")
        print(f"DICT {request.form.to_dict(flat=False)}")
        
        return "OK", 201