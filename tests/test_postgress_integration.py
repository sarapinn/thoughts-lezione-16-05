import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

import pytest
from app import create_app
from extensions import db
from models import ThoughtModel

@pytest.fixture
def app_context():
    config = {
        "SQLALCHEMY_DATABASE_URI": os.environ.get("DATABASE_URL"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }
    app = create_app(config)

   
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_db_integration(app_context):
    # Create a new thought
    thought = ThoughtModel(username="postgress_user", text="Dato")
    db.session.add(thought)
    db.session.commit()

    result = ThoughtModel.query.filter_by(username="postgress_user").first()
    assert result is not None
    assert result.text == "Dato"

    