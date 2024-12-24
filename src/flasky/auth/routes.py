from src.flasky.auth import bp
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from src.pybet import schema
from src.flasky.auth.forms.login_form import LoginForm
from src.flasky.auth.forms.register_form import RegisterForm
from flask import redirect, render_template, flash, url_for
from src import config
from src.pybet import unit_of_work

@bp.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        uow = unit_of_work.SqlAlchemyUnitOfWork(config.get_session_factory())
        with uow:
            user = uow.session.scalar(
                sa.select(schema.User).where(schema.User.username == form.username.data))
            
            if user is None or not user.check_password(form.password.data):
                flash("Wrong credentials", category="error")
                return redirect(url_for('auth.login_view'))
            
            login_user(user)
            return redirect('/index')
    return render_template('login.html', title='Login', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    
    if form.validate_on_submit():
        uow = unit_of_work.SqlAlchemyUnitOfWork(config.get_session_factory())
        
        with uow:
            user = schema.User(username = form.username.data)
            user.set_password(password = form.password.data)
            
            uow.session.add(user)
            uow.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth.login_view'))
    
    return render_template('register.html', title='Register', form=form)

@bp.route('/logout', methods=['POST'])
def logout_view():
    
    logout_user()
    return redirect('/index')