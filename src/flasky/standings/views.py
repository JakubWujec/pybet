from src.flasky.standings import bp
from src.pybet import unit_of_work
from flask import render_template

@bp.route("/standings", methods=["GET"])
def standings_view():
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    standings = [
        {
            "position": 1,
            "name": "Adam",
            "points": 100
        },
        {
            "position": 2,
            "name": "Bob",
            "points": 99
        },
        {
            "position": 3,
            "name": "Eva",
            "points": 45
        },
        
    ]
    
    return render_template(
        'standings.html',
        standings=standings
    )
