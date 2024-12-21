from flask import Flask, request, render_template, flash, redirect
from src.pybet import schema
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.config import Config, get_session
from src.flasky.admin import views as admin_views
from src import config


login = LoginManager()

def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login.init_app(app)    
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    schema.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    admin = Admin(
        app, 
        name='pybet',

    )
    admin.add_view(admin_views.PybetAdminModelView(schema.Match, session))
    admin.add_view(admin_views.PybetAdminModelView(schema.User, session))


    from src.flasky.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from src.flasky.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from src.flasky.matches import bp as matches_bp
    app.register_blueprint(matches_bp)
    
    from src.flasky.mybet import bp as mybet_bp
    app.register_blueprint(mybet_bp)


    return app

@login.user_loader
def load_user(id):
    return get_session().get(schema.User, int(id))