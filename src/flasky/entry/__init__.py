from flask import Blueprint

bp = Blueprint('entry', __name__, template_folder="./templates")

from src.flasky.entry import views


