from flask import Blueprint

bp = Blueprint("my-bet", __name__)

from flasky.mybet import views
