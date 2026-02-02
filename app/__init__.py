from flask import Flask
from .extensions import db, migrate
from .routes import main

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)

    return app

