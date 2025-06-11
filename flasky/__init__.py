from flask import Flask, url_for
from pybet import schema
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import LoginManager
from flasky.admin import views as admin_views
from config import session_scope, get_db_engine, Config
from flask_sqlalchemy import SQLAlchemy

login = LoginManager()
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    login.login_view = "auth.login_view"
    login.login_message = "Please log in to access this page."
    login.login_message_category = "warning"

    engine = get_db_engine()
    schema.metadata.create_all(engine)

    admin = Admin(
        app,
        name="pybet",
    )
    admin.add_view(admin_views.PybetAdminModelView(schema.Team, db.session))
    admin.add_view(
        admin_views.AdminMatchView(
            schema.Match, db.session, name="Manage Matches", endpoint="manage_matches"
        )
    )
    admin.add_view(
        admin_views.UpdateScoreView(
            schema.Match, db.session, name="Update Score", endpoint="update_scores"
        )
    )
    admin.add_view(admin_views.PybetAdminModelView(schema.User, db.session))
    admin.add_view(admin_views.PybetAdminModelView(schema.Bet, db.session))
    admin.add_view(admin_views.PybetAdminModelView(schema.Gamestage, db.session))
    admin.add_link(MenuLink(name="Back to App", category="", url="/"))

    from flasky.main import bp as main_bp

    app.register_blueprint(main_bp)

    from flasky.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from flasky.mybet import bp as mybet_bp

    app.register_blueprint(mybet_bp)

    from flasky.standings import bp as standings_bp

    app.register_blueprint(standings_bp)

    from flasky.points import bp as points_bp

    app.register_blueprint(points_bp)

    from flasky.generic.errors import page_not_found, internal_error, forbidden_error

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(403, forbidden_error)

    return app


@login.user_loader
def load_user(id):
    u = db.session.get(schema.User, int(id))
    return u
