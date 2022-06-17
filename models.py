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
        db.ForeignKey("users.id"),
        nullable=false)

    user = db.relationship("User",backref='posts')


class Tag (db.model):
    """Create tag instances"""

    __tablename__= 'tags'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(
        db.String(50),
        nullable=false,
        Unique=True
        )


class PostTag (db.model):
    """Create PostTag instances"""

    __tablename__= 'posttags'
    # tag_id
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True,
        nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True,
        nullable=False)

    tag = db.relationship("Tag",backref='posttags')
    post = db.relationship("Post",backref = 'posttags')







