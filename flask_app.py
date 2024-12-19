from flask import Flask, request, render_template
from src.pybet import schema, unit_of_work, handlers
from src.pybet import config, message_bus, commands
import datetime

app = Flask(__name__, template_folder="src/templates")


@app.route("/bets", methods=["POST"])
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

@app.route("/matches", methods=["POST"])
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

@app.route("/matches/<match_id>", methods=["POST"])
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

@app.route("/")
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

if __name__ == "__main__":
    #flask --app flask_app run --host=localhost --port=5005 
    app.run(host="localhost", port=5005, debug=True)
    
