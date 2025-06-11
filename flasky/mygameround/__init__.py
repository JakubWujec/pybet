from flask import Blueprint

bp = Blueprint("mygameround", __name__)

from flasky.mygameround import views
