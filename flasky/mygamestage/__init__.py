from flask import Blueprint

bp = Blueprint("mygamestage", __name__)

from flasky.mygamestage import views
