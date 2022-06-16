"""Models for Blogly."""

from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, false
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User (db.Model):
    """User."""
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(
        db.String(50),
        nullable=false)
    last_name = db.Column(
        db.String(50),
        nullable=false)
    image_url = db.Column(
        db.Text)


class Post (db.Model):
    """Create post instances"""

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    title = db.Column(
        db.String(50),
        nullable=false)
    content = db.Column(
        db.Text,
        nullable=false)
    created_at=db.Column(
        db.DateTime,
        nullable=false,
        default=db.func.now())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"))

    user = db.relationship("User",backref='posts')





