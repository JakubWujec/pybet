from src.flasky.mybet import bp
from src.pybet import schema, unit_of_work, queries
from src.pybet import message_bus, commands
from flask import request, render_template, flash, redirect
from src.flasky.forms.bet_form import BetForm
from src.flasky.forms.match_form import MatchForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime
from src.config import get_session
from src.flasky.mybet import forms

@bp.route("/my-bets", methods=["GET", "POST"])
@login_required
def mybets_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    matches = queries.mybets(current_user.id, uow)
    form = forms.MatchBetListForm()

    if request.method == "GET":
        for match in matches:
            form.bets.append_entry({
                "match_id": int(match["id"]),
                "home_team_score":0,
                "away_team_score":0
            })
  
    if request.method == "POST":
    
        if form.validate_on_submit():
            cmds = []
            # Process bets
            print(form.data)
            for bet in form.data["bets"]:
                cmds.append(commands.MakeBetCommand(
                    user_id=current_user.id,
                    match_id=bet['match_id'],
                    home_team_score=bet['home_team_score'],
                    away_team_score=bet['away_team_score'],
                ))
                print(f"BET: {bet}")
            with uow:
                for message in cmds:
                    message_bus.handle(message, uow)
          

        return "OK", 201
            
        

    return render_template(
        'mybet.html',
        current_user=current_user,
        matches=matches,
        enumerate=enumerate,
        form=form
    )
