from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

class MatchForm(FlaskForm):
    home_team_id = IntegerField('Home team', validators=[DataRequired()])
    away_team_id = IntegerField('Away team', validators=[DataRequired()])
    submit = SubmitField('Make a bet')