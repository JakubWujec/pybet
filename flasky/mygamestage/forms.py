from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput


class HiddenInteger(IntegerField):
    widget = HiddenInput()


def non_negative_integer_required(form, field):
    if field.data is None or field.data < 0:
        raise ValidationError("Field must be non-negative integer.")


# Subform for individual matches
class MatchBetForm(Form):
    match_id = HiddenInteger(validators=[DataRequired()])
    home_team_score = IntegerField(
        "Home Score", validators=[non_negative_integer_required]
    )
    away_team_score = IntegerField(
        "Away Score", validators=[non_negative_integer_required]
    )


# Main form to hold all matches
class MatchBetListForm(FlaskForm):
    bets = FieldList(FormField(MatchBetForm))  # Dynamic list of MatchBetForm
    submit = SubmitField("Submit Bets")
