from flask import Blueprint

bp = Blueprint('points', __name__)

from flasky.points import views


