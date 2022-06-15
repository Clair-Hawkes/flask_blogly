"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
db = SQLAlchemy()

class User (db.Model):
    """Docstring????"""
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(
        db.String(50),
        nullable =false)
    last_name = db.Column(
        db.string(50),
        nullable = false)
    image_url = db.Column(
        db.string(500),
        nullable = false)

