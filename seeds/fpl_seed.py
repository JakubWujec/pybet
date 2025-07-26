from pybet import schema
from sqlalchemy.orm import Session
from datetime import datetime
from config import session_scope
import requests


def seed_teams_and_matches_from_fpl(session: Session):
    URL1 = "https://fantasy.premierleague.com/api/bootstrap-static/"
    URL2 = "https://fantasy.premierleague.com/api/fixtures/"
    fpl_teams = {}

    r = requests.get(url=URL1)
    data = r.json()
    teams_data = data["teams"]
    for row in teams_data:
        short_name = row["short_name"]
        team = schema.Team(name=short_name)
        session.add(team)
        fpl_teams[row["id"]] = team

    session.flush()

    gamestages = {}
    for i in range(1, 39):
        gamestages[i] = schema.Gamestage(id=i, name=f"Gamestage {i}")
        session.add(gamestages[i])

    session.flush()

    r = requests.get(url=URL2)
    fixtures_data = r.json()
    for idx, fixture in enumerate(fixtures_data):
        if not fixture["finished"] and fixture["event"] is not None:
            team_a = fpl_teams[fixture["team_a"]]
            team_h = fpl_teams[fixture["team_h"]]
            match = schema.Match(
                home_team_id=team_h.id,
                away_team_id=team_a.id,
                kickoff=fromisoformat(fixture["kickoff_time"]),
                gamestage_id=fixture["event"],
            )
            session.add(match)

    session.commit()


def fromisoformat(date_str: str):
    # py3.10 datetime doesn't parse dates with Z properly, ex. 2025-01-14T19:30:00Z
    if "Z" in date_str:
        date_str = date_str.replace("Z", "+00:00")
    return datetime.fromisoformat(date_str)


if __name__ == "__main__":
    with session_scope() as session:
        seed_teams_and_matches_from_fpl(session)
