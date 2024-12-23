from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, HiddenField, SubmitField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, NumberRange

class HiddenInteger(IntegerField):
    widget = HiddenInput()

# Subform for individual matches
class MatchBetForm(Form):
    match_id = IntegerField(validators=[DataRequired()])
    home_team_score = IntegerField("Home Score", validators=[DataRequired(), NumberRange(min=0)], default=0)
    away_team_score = IntegerField("Away Score", validators=[DataRequired(), NumberRange(min=0)], default=0)

# Main form to hold all matches
class MatchBetListForm(FlaskForm):
    bets = FieldList(FormField(MatchBetForm))  # Dynamic list of MatchBetForm
    submit = SubmitField("Submit Bets")