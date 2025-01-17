from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from src.pybet import schema
from src.config import get_session
import sqlalchemy as sa

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        session = get_session()
        user = session.scalar(sa.select(schema.User).where(
            schema.User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
        
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    rememberMe = BooleanField()
    submit = SubmitField('Login')