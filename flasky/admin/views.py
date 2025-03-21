import flask_login as login
from flask import request, flash
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from pybet import commands, message_bus, unit_of_work, events

class PybetAdminModelView(ModelView):
    def is_accessible(self):
        return login.current_user and login.current_user.is_authenticated and login.current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login_view"))
    

class AdminMatchView(PybetAdminModelView):
    column_list = [
        'id',
        'home_team',
        'away_team',
        'home_team_score',
        'away_team_score',
        'kickoff',
        'gameround'
    ]
    
    form_columns = [
        'home_team',
        'away_team',
        'kickoff',
        'gameround'
    ]
    
    column_filters=['gameround', 'home_team', 'away_team']
    
  
class UpdateScoreView(PybetAdminModelView):    
    can_delete = False
    can_create = False
    can_view_details = False
    column_list = [
        'id',
        'home_team',
        'away_team',
        'home_team_score',
        'away_team_score',
        'kickoff',
        'gameround'
    ]
    
    form_columns = [
        'home_team_score',
        'away_team_score',
    ]
    
    column_filters=['gameround', 'home_team',  'away_team']
    
    def update_model(self, form, model):
        uow = unit_of_work.SqlAlchemyUnitOfWork(lambda: self.session)
        message_bus.handle(
            commands.UpdateMatchScoreCommand(
                model.id,
                form.data['home_team_score'],
                form.data['away_team_score'],
            ),
            uow
        )
    
        return True