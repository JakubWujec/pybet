from flask import Flask, request, render_template, flash, redirect
from src.flasky.flask_config import FlaskConfig

def create_app(config_class=FlaskConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from src.flasky.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app