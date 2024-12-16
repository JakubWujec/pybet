from src.pybet import unit_of_work
from src.pybet import model
from sqlalchemy.sql import text
from sqlalchemy.engine import CursorResult


def get_linked_bet_id(session, user_id, match_id):
    cursorResult: CursorResult = session.execute(text(
        'SELECT bets.id FROM bets WHERE bets.match_id=:match_id and bets.user_id=:user_id',
    ), dict(user_id=user_id, match_id=match_id))
    
    return cursorResult.first()

def test_uow_can_retrieve_match_and_place_a_bet_to_it(session_factory):
    session = session_factory() 
    user_id = 1
    match_id = 1
    
    session.execute(
        text(
        "INSERT INTO matches (home_team_id, away_team_id)"
        ' VALUES (1, 2)')
    )
    session.execute(
        text(
        "INSERT INTO users (username)"
        ' VALUES (:username)'),
        dict(username="Bob")
    )
    session.commit()
    
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        match: model.Match = uow.matches.get(match_id=match_id)
        assert match is not None
        match.place_bet(
            user_id=user_id,
            home_team_score=2,
            away_team_score=3
        )
        print(f"XXXXX {match.bets}")
        print(vars(uow.session))
        print("AA")
        uow.commit()
        print(f"XXXXX {match.bets}")
    result = session.execute(
        text(
        "SELECT * FROM bets"),
    )    
    
    for row in result:
        print(f"RESULTROW {row}")

    
    bet_id = get_linked_bet_id(session, user_id, match_id)
    
    assert bet_id is not None
        