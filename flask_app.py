from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.pybet import orm, repository, model, services
from src.pybet import config

app = Flask(__name__)
orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_sqlite_uri()))

@app.route("/bets", methods=["POST"])
def make_a_bet():
    session = get_session()
    repo = repository.SqlMatchRepository(session)
    user_id = 1

    services.make_bet(
        user_id,
        request.json["match_id"],
        request.json["home_team_score"],
        request.json["away_team_score"],
        repo,
        session
    )
    
    return "OK", 201

@app.route("/matches", methods=["POST"])
def create_match():
    session = get_session()
    repo = repository.SqlMatchRepository(session)

    repo.add(
        model.Match(
            home_team_id=request.json["home_team_id"],
            away_team_id=request.json["away_team_id"],
        )
    )
    
    print(vars(repo.list()[0]))
   
    return "OK", 201

if __name__ == "__main__":
    #flask --app flask_app run --host=localhost --port=5005 
    app.run(host="localhost", port=5005, debug=True)
    
