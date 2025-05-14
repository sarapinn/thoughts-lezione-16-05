from flask import Flask
from flask_restx import Api

from extensions import db
from resources.thoughts import api as thoughts_ns

def create_app(config_overrides=None):

    app = Flask(__name__)

    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///thoughts.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:adminpass@db/thoughtsdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    api = Api(app, version="1.0", title="Thoughts API", description="REST API")
    api.add_namespace(thoughts_ns)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)