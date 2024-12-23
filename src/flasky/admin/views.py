import flask_login as login
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for

class PybetAdminModelView(ModelView):
    def is_accessible(self):
        return login.current_user and login.current_user.is_authenticated and login.current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login_view"))
    

class AdminMatchView(ModelView):
    column_list = [
        'id',
        'home_team',
        'away_team',
        'home_team_score',
        'away_team_score',
        'kickoff'
    ]
    
    form_columns = [
        'home_team',
        'away_team',
        'kickoff',
    ]
    
  