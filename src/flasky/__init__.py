from flask import Flask, request, render_template, flash, redirect
from src.pybet import schema
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from src.flasky.admin import views as admin_views
from src import config


login = LoginManager()

def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login.init_app(app)    
    engine = config.get_db_engine()
    schema.metadata.create_all(engine)
    
    with config.session_scope() as session:
        admin = Admin(
            app, 
            name='pybet',

        )
        admin.add_view(admin_views.PybetAdminModelView(schema.Team, session))
        admin.add_view(admin_views.AdminMatchView(schema.Match, session))
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
    return config.get_session().get(schema.User, int(id))