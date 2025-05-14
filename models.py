from datetime import datetime, UTC
from extensions import db

class ThoughtModel(db.Model):
    __tablename__ = "thoughts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda:datetime.now(UTC))
