from flask import Blueprint

bp = Blueprint('matches', __name__, template_folder="./templates")

from src.flasky.matches import views