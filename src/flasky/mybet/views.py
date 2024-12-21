from src.flasky.mybet import bp
from src.pybet import schema, unit_of_work
from src.pybet import message_bus, commands
from flask import request, render_template, flash, redirect
from src.flasky.forms.bet_form import BetForm
from src.flasky.forms.match_form import MatchForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime


@bp.route("/my-bet", methods=["GET", "POST"])
def mybet_view():
    # form = BetForm()
    
    # if form.validate_on_submit():
    #     uow = unit_of_work.SqlAlchemyUnitOfWork()
    #     message_bus.handle(
    #         commands.MakeBetCommand(
    #             user_id=current_user.id,
    #             match_id=match_id,
    #             home_team_score=form.home_team_score.data,
    #             away_team_score=form.away_team_score.data,
    #         ),
    #         uow
    #     )
    #     flash('Submitted data {}, remember_me={}'.format(
    #         form.home_team_score.data, form.away_team_score.data))
    #     return redirect('/index')
    
    return render_template(
        'mybet.html',
    )