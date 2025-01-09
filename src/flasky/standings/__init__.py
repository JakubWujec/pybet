from flask import Blueprint

bp = Blueprint('standings', __name__, template_folder="./templates")

from src.flasky.standings import views