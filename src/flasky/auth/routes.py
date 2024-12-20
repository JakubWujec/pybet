from src.flasky.auth import bp
from flask_login import current_user, login_user
import sqlalchemy as sa
from src.pybet import schema
from src.flasky.forms.login_form import LoginForm
from flask import redirect, render_template, flash, url_for


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = db.session.scalar(
    #         sa.select(schema.User).where(schema.User.username == form.username.data))
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)