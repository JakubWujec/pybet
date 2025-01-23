from flask import Blueprint

bp = Blueprint('auth', __name__)

from flasky.auth import routes