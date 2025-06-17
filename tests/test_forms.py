from flasky.mygamestage.forms import MatchBetForm
from werkzeug.datastructures import MultiDict


def test_negative_score():
    """Test the form with a negative score."""
    form_data = MultiDict(
        {
            "match_id": 1,
            "home_team_score": -1,  # Invalid negative score
            "away_team_score": 3,
        }
    )
    form = MatchBetForm(formdata=form_data)
    assert not form.validate(), "The form should not validate with a negative score."
    assert "home_team_score" in form.errors, "home_team_score should have an error."


def test_should_throw_when_home_score_too_high():
    """Test the form with a too high score."""
    form_data = MultiDict(
        {
            "match_id": 1,
            "home_team_score": 101,  # Invalid negative score
            "away_team_score": 3,
        }
    )
    form = MatchBetForm(formdata=form_data)
    assert not form.validate(), "The form should not validate with a score over 100."
    assert "home_team_score" in form.errors, "home_team_score should have an error."


def test_should_throw_when_away_score_too_high():
    """Test the form with a too high score."""
    form_data = MultiDict(
        {
            "match_id": 1,
            "home_team_score": 3,  # Invalid negative score
            "away_team_score": 101,
        }
    )
    form = MatchBetForm(formdata=form_data)
    assert not form.validate(), "The form should not validate with a score over 100."
    assert "away_team_score" in form.errors, "home_team_score should have an error."


def test_valid():
    """Test the form with valid data."""
    form_data = MultiDict(
        {
            "match_id": 1,
            "home_team_score": 1,
            "away_team_score": 2,
        }
    )
    form = MatchBetForm(formdata=form_data)

    assert form.validate(), f"The form should validate with valid data. {form.errors}"


def test_valid_form_when_nil_nil_score():
    """Test the form with valid data."""
    form_data = MultiDict(
        {
            "match_id": 1,
            "home_team_score": 0,
            "away_team_score": 0,
        }
    )
    form = MatchBetForm(formdata=form_data)
    if not form.validate():
        for field_name, error_messages in form.errors.items():
            print(f"Field '{field_name}' errors: {', '.join(error_messages)}")
    print(form.data)

    print(form.home_team_score.data)
    assert form.validate(), "The form should validate with 0:0 score."


def test_form_shouldnt_validate_without_scores():
    """Test the form with missing scores."""
    form_data = MultiDict(
        {
            "match_id": 1,
        }
    )
    form = MatchBetForm(formdata=form_data)
    assert not form.validate(), "The form should not validate with missing scores."
    assert "home_team_score" in form.errors, "home_team_score should have an error."
    assert "away_team_score" in form.errors, "away_team_score should have an error."
