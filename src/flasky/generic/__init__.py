from flask import Blueprint

bp = Blueprint('generic', __name__)

from src.flasky.generic import views