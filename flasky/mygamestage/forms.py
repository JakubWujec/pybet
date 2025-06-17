from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput


class HiddenInteger(IntegerField):
    widget = HiddenInput()


MAX_SCORE = 100


def score_range_validator(form: "MatchBetForm", field: IntegerField):
    if field.data is None or field.data > MAX_SCORE or field.data < 0:
        raise ValidationError(f"{field.label.text} must be between 0 and {MAX_SCORE}.")


# Subform for individual matches
class MatchBetForm(Form):
    match_id = HiddenInteger(validators=[DataRequired()])
    home_team_score = IntegerField(
        label="Home Score",
        validators=[score_range_validator],
    )
    away_team_score = IntegerField(
        label="Away Score", validators=[score_range_validator]
    )


# Main form to hold all matches
class MatchBetListForm(FlaskForm):
    bets = FieldList(FormField(MatchBetForm))  # Dynamic list of MatchBetForm
    submit = SubmitField("Submit Bets")
