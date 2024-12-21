from flask import Blueprint

bp = Blueprint('my-bet', __name__, template_folder="./templates")

from src.flasky.mybet import views


