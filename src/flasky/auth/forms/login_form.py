from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    rememberMe = BooleanField()
    submit = SubmitField('Login')