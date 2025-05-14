import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

import pytest
from freezegun import freeze_time
from app import create_app
from extensions import db
from models import ThoughtModel

@pytest.fixture
def client():
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }
    app = create_app(config)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_get_empty_thoughts(client):
    response = client.get("/thoughts/")
    assert response.status_code == 200
    assert response.json == []

@freeze_time("2024-01-01")
def test_post_thought_valid_token(client):
    data = {"username":"mario", "text":"Ciao"}
    headers = {"Authorization": "Bearer valid-token"}
    response = client.post("/thoughts/", json=data, headers=headers)
    assert response.status_code == 201
    json_data = response.json
    assert json_data["username"] == "mario"
    assert json_data["text"] == "Ciao"
    assert json_data["timestamp"].startswith("2024-01-01")


def test_post_thought_invalid_token(client):
    data = {"username":"mario", "text":"Ciao"}
    headers = {"Authorization": "Bearer wrong-token"}
    response = client.post("/thoughts/", json=data, headers=headers)
    assert response.status_code == 401

def test_get_thought_by_id(client):
    with client.application.app_context():
        t = ThoughtModel(username="anna", text="test")
        db.session.add(t)
        db.session.commit()
        tid = t.id

    response = client.get(f"/thoughts/{tid}")
    assert response.status_code == 200
    assert response.json["username"] == "anna"