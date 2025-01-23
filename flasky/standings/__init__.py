from flask import Blueprint

bp = Blueprint('standings', __name__, template_folder="./templates")

from flasky.standings import views