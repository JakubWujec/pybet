from flask import Flask, request, render_template, flash, redirect
from src.pybet import schema
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.config import Config 

from src import config

def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    schema.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    admin = Admin(app, name='pybet')
    admin.add_view(ModelView(schema.Match, session))
    admin.add_view(ModelView(schema.User, session))

    from src.flasky.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app