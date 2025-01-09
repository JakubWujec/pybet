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
        admin.add_view(admin_views.AdminMatchView(schema.Match, session, name="Manage Matches",endpoint="manage_matches"))
        admin.add_view(admin_views.UpdateScoreView(schema.Match, session, name="Update Score", endpoint="update_scores"))
        admin.add_view(admin_views.PybetAdminModelView(schema.User, session))


    from src.flasky.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from src.flasky.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from src.flasky.mybet import bp as mybet_bp
    app.register_blueprint(mybet_bp)
    
    from src.flasky.entry import bp as entry_bp
    app.register_blueprint(entry_bp)
    
    from src.flasky.standings import bp as standings_bp
    app.register_blueprint(standings_bp)
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)


    return app

@login.user_loader
def load_user(id):
    with config.session_scope() as session:
        u = session.get(schema.User, int(id))
        if u is not None:
            return schema.User(id=u.id, username=u.username, password_hash=u.password_hash, role=u.role)
        return u
    
def page_not_found(error):
    return render_template('404.html'), 404

def internal_error(error):
    return render_template('500.html'), 500