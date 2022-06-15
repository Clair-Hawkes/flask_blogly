"""Blogly application."""

from flask import Flask, render_template
from models import db, connect_db,User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

@app.get('/')
def index():
    """List users and show homepage"""

    users = User.query.all()
    return render_template("index.html",users=users)


