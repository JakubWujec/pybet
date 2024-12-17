from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.pybet import schema, services, unit_of_work
from src.pybet import config

app = Flask(__name__)


@app.route("/bets", methods=["POST"])
def make_a_bet():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user_id = 1

    services.make_bet(
        user_id=user_id,
        match_id=request.json["match_id"],
        home_team_score=request.json["home_team_score"],
        away_team_score=request.json["away_team_score"],
        uow=uow
    )
    
    return "OK", 201

@app.route("/matches", methods=["POST"])
def create_match():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        uow.matches.add(
            schema.Match(
                home_team_id=request.json["home_team_id"],
                away_team_id=request.json["away_team_id"],
            )
        )
        uow.commit()
   
    return "OK", 201

@app.route("/matches/<match_id>", methods=["POST"])
def update_score(match_id):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    
    services.update_match_score(
        match_id,
        home_team_score=request.json["home_team_score"],
        away_team_score=request.json["home_team_score"],
        uow=uow
    )
    
    return "OK", 201

if __name__ == "__main__":
    #flask --app flask_app run --host=localhost --port=5005 
    app.run(host="localhost", port=5005, debug=True)
    
