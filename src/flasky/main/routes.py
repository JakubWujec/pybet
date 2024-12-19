from src.flasky.main import bp
from src.pybet import schema, unit_of_work
from src.pybet import message_bus, commands
from flask import request, render_template, flash, redirect
from src.flasky.forms.bet_form import BetForm
import datetime

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

@bp.route("/matches/<match_id>/bet", methods=["GET", "POST"])
def make_a_bet_form(match_id):
    form = BetForm()
    
    if form.validate_on_submit():
        flash('Submitted data {}, remember_me={}'.format(
            form.home_team_score.data, form.away_team_score.data))
        return redirect('/index')
    
    return render_template(
        'make_bet.html',
        form=form
    )

@bp.route("/testme")
def testme():
    return "TEST SUCCEED", 201


@bp.route("/")
@bp.route("/index")
def index():
    user = {'username': 'John'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
