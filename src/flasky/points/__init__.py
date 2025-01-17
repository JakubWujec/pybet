from flask import Blueprint

bp = Blueprint('points', __name__)

from src.flasky.points import views


