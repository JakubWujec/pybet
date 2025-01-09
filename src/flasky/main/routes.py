from src.flasky.main import bp
from src.pybet import schema, unit_of_work
from src.pybet import message_bus, commands
from src.pybet import queries
from flask import request, render_template, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required
import datetime

@bp.route('/points', methods=['GET'])
@login_required
def points():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = current_user.id
    gameround_id = queries.get_current_gameround_id(uow)
    return redirect(f'/entry/{user_id}/rounds/{gameround_id}')

@bp.route("/api/bets", methods=["POST"])
def make_a_bet():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = 1

    message_bus.handle(
        commands.MakeBetCommand(
            user_id=user_id,
            match_id=request.json["match_id"],
            home_team_score=request.json["home_team_score"],
            away_team_score=request.json["away_team_score"],
        ),
        uow
    )
    
    return "OK", 201

@bp.route("/api/matches", methods=["POST"])
def create_match():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    
    kickoff = request.json["kickoff"]
    if kickoff is not None:
        kickoff = datetime.datetime.fromisoformat(kickoff)

    with uow:
        uow.matches.add(
            schema.Match(
                home_team_id=request.json["home_team_id"],
                away_team_id=request.json["away_team_id"],
                kickoff=kickoff
            )
        )
        uow.commit()
   
    return "OK", 201

@bp.route("/api/matches/<match_id>", methods=["POST"])
def update_score(match_id):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    
    message_bus.handle(
        commands.UpdateMatchScoreCommand(
            match_id=match_id,
            home_team_score=request.json["home_team_score"],
            away_team_score=request.json["home_team_score"],
        ),
        uow
    )
    
    return "OK", 201
    
@bp.route("/testme")
def testme():
    return "TEST SUCCEED", 201


@bp.route("/")
@bp.route("/index")
def index():
    user = current_user
    username = None
    if not current_user.is_anonymous:
        username = user.username
    return render_template('index.html', title='Home', username=username )
