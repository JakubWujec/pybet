from flask import Blueprint

bp = Blueprint('my-bet', __name__)

from src.flasky.mybet import views


