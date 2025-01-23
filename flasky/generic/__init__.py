from flask import Blueprint

bp = Blueprint('generic', __name__)

from flasky.generic import views