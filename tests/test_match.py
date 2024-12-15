from src.pybet import model

def test_can_create_match():
    match = model.Match(1, 2)
    
    assert match is not None
    assert isinstance(match, model.Match)
    
