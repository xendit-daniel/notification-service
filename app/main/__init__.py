
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

from .config import config_by_name
from flask.app import Flask

db = SQLAlchemy()
Base = declarative_base()

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.url_map.strict_slashes = False
    db.init_app(app)

    return app