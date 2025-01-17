from flask import Blueprint

bp = Blueprint('auth', __name__)

from src.flasky.auth import routes