from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

class BetForm(FlaskForm):
    home_team_score = IntegerField('Home team score', validators=[DataRequired()])
    away_team_score = IntegerField('Away team score', validators=[DataRequired()])
    submit = SubmitField('Make a bet')