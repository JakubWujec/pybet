from sqlalchemy.sql import text

def test_saving_match(session):
    session.execute(
        text(
        "INSERT INTO matches (home_team_id, away_team_id)"
        ' VALUES (1, 2)')
    )
    session.commit()
    
    rows = list(session.execute(text('SELECT home_team_id, away_team_id FROM "matches"')))
    assert rows == [(1, 2)]
    
