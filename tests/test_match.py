from src.pybet import schema

def test_can_create_match():
    match = schema.Match(
        home_team_id=1, 
        away_team_id=2
    )
    
    assert match is not None
    assert isinstance(match, schema.Match)
    
