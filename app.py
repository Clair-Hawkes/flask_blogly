"""Blogly application."""

from flask import Flask, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def index():
    """Redirect to users route"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """List users and show homepage."""

    users = User.query.all()
    return render_template("users.html",users=users)

@app.get('/users/new')
def add_user():
    """Show form."""

    return render_template("add_user.html")
