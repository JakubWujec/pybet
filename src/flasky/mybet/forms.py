from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, HiddenField, SubmitField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, NumberRange, InputRequired, ValidationError

class HiddenInteger(IntegerField):
    widget = HiddenInput()

def non_negative_integer_required(form, field):
    if field.data is None or field.data < 0:
        raise ValidationError("Field must be non-negative integer.")

# Subform for individual matches
class MatchBetForm(Form):
    match_id = IntegerField(validators=[DataRequired()])
    home_team_score = IntegerField("Home Score", validators=[non_negative_integer_required])
    away_team_score = IntegerField("Away Score", validators=[non_negative_integer_required])

# Main form to hold all matches
class MatchBetListForm(FlaskForm):
    bets = FieldList(FormField(MatchBetForm))  # Dynamic list of MatchBetForm
    submit = SubmitField("Submit Bets")