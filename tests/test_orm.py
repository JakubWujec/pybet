from sqlalchemy.sql import text


def test_saving_match(session):
    HOME_TEAM_ID = 1
    AWAY_TEAM_ID = 2
    session.execute(
        text(
            f"INSERT INTO matches (home_team_id, away_team_id) VALUES ({HOME_TEAM_ID}, {AWAY_TEAM_ID})"
        )
    )
    session.commit()

    rows = list(
        session.execute(text('SELECT home_team_id, away_team_id FROM "matches"'))
    )
    assert rows == [(HOME_TEAM_ID, AWAY_TEAM_ID)]
