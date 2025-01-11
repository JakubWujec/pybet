from flask import Blueprint

bp = Blueprint('points', __name__, template_folder="./templates")

from src.flasky.points import views


