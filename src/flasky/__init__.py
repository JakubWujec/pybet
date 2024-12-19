from flask import Flask, request, render_template, flash, redirect
from src import config

def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from src.flasky.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app