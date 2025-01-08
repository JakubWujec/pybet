from src.pybet import unit_of_work
from src.pybet import schema
from sqlalchemy.sql import text
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.session import Session, sessionmaker

def get_linked_bet_id(session: Session, user_id: int, match_id: int) -> int | None:
    cursorResult: CursorResult = session.execute(
        text(
            'SELECT bets.id FROM bets WHERE bets.match_id=:match_id and bets.user_id=:user_id'
        ),
        dict(user_id=user_id, match_id=match_id)
    )

    return cursorResult.first()

def insert_user_and_match(session):
    session.execute(
            text(
            "INSERT INTO matches (home_team_id, away_team_id, gameround_id)"
            ' VALUES (1, 2, 1)')
        )
    session.execute(
            text(
            "INSERT INTO users (username)"
            ' VALUES (:username)'),
            dict(username="Bob")
        )

def test_uow_can_retrieve_match_and_place_a_bet_to_it(in_memory_sqlite_session_factory: sessionmaker):
    user_id = 1
    match_id = 1
    
    session = in_memory_sqlite_session_factory()
    insert_user_and_match(session)
    session.commit()
    uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
    
    with uow:
        match: schema.Match = uow.matches.get(match_id=match_id)
        assert match is not None
        
        bet = schema.Bet(
            user_id=user_id,
            match_id = match.id,
            home_team_score=2,
            away_team_score=3
        )
        match.place_bet(bet)

        uow.commit()
        
    bet_id = get_linked_bet_id(in_memory_sqlite_session_factory(), user_id, match_id)
    
    assert bet_id is not None
        
def test_rolls_back_uncommitted_work_by_default(in_memory_sqlite_session_factory: sessionmaker):
    user_id = 1
    match_id = 1
    session = in_memory_sqlite_session_factory()
    insert_user_and_match(session)
    session.commit()
    
    uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
    with uow:
        match: schema.Match = uow.matches.get(match_id=match_id)
        bet = schema.Bet(
            user_id=user_id,
            match_id = match.id,
            home_team_score=2,
            away_team_score=3
        )
        match.place_bet(bet)
        
    new_session = in_memory_sqlite_session_factory()
    rows = list(new_session.execute(text('SELECT * FROM "bets"')))
    assert rows == []
        