from flask_admin import expose
import flask_admin as admin
import flask_login as login
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for

class PybetAdminIndexView(admin.AdminIndexView):
    @expose("/")
    def index(self):
        print(vars(login.current_user))
        print(login.current_user.is_admin())
        if not login.current_user.is_admin():
            return redirect(url_for("auth.login_view"))
        return super().index()

class PybetAdminModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login_view"))