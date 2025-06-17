from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput


class HiddenInteger(IntegerField):
    widget = HiddenInput()


MAX_SCORE = 100


def non_negative_integer_required(form, field):
    if field.data is None or field.data < 0:
        raise ValidationError(f"{field.label.text} must be non-negative integer.")


def too_high_value(form: "MatchBetForm", field: IntegerField):
    if field.data is None or field.data > MAX_SCORE:
        raise ValidationError(
            f"{field.label.text} must be non-negative integer less than {MAX_SCORE}."
        )


# Subform for individual matches
class MatchBetForm(Form):
    match_id = HiddenInteger(validators=[DataRequired()])
    home_team_score = IntegerField(
        label="Home Score",
        validators=[non_negative_integer_required, too_high_value],
    )
    away_team_score = IntegerField(
        label="Away Score", validators=[non_negative_integer_required, too_high_value]
    )


# Main form to hold all matches
class MatchBetListForm(FlaskForm):
    bets = FieldList(FormField(MatchBetForm))  # Dynamic list of MatchBetForm
    submit = SubmitField("Submit Bets")
