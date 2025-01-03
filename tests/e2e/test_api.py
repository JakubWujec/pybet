import pytest
import requests
from src.pybet import config
import datetime

def post_to_add_match(home_team_id: int, away_team_id: int, kickoff = datetime.datetime.now() + datetime.timedelta(days=1)):
    url = config.get_api_url()
    r = requests.post(
        f"{url}/api/matches", json={"home_team_id": home_team_id, "away_team_id": away_team_id, "kickoff": datetime.datetime.isoformat(kickoff)}
    )
    assert r.status_code == 201

@pytest.mark.usefixtures("sqlite_db")
@pytest.mark.usefixtures("restart_api")
def test_make_bet_happy_path_returns_201():
    post_to_add_match(1, 2, kickoff=datetime.datetime.now() + datetime.timedelta(days=1))
    
    data = {
        "match_id": 1,
        "home_team_score": 2,
        "away_team_score": 3}
    url = config.get_api_url()

    r = requests.post(f"{url}/api/bets", json=data)

    assert r.status_code == 201


@pytest.mark.usefixtures("sqlite_db")
@pytest.mark.usefixtures("restart_api")
def test_update_match_score_happy_path_returns_201():
    post_to_add_match(1, 2)
    
    data = {
        "match_id": 1,
        "home_team_score": 2,
        "away_team_score": 3}
    url = config.get_api_url()

    r = requests.post(f"{url}/api/matches/1", json=data)

    assert r.status_code == 201
