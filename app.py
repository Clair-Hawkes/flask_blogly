"""Blogly application."""

from flask import Flask, render_template, redirect, request
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
    return render_template("users.html", users=users)


@app.get('/users/new')
def add_user_page():
    """Show form."""

    return render_template("add_user.html")


@app.post('/users/new')
def add_user():
    """Hi."""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['img-url']
    image_url = str(image_url) if image_url else None

    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def user_page(user_id):
    """Show user page per user details"""

    user_record = User.query.get(user_id)

    return render_template('user_page.html', user=user_record)


@app.get('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    """Show user page per user details"""

    user_record = User.query.get(user_id)

    if not user_record.image_url:
        user_record.image_url = ""

    return render_template('edit_user.html', user=user_record)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show user page per user details"""

    user = User.query.get(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']
    user.image_url = str(user.image_url) if user.image_url else None

    db.session.commit()


    return redirect('/users')

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete User commits updatr to DB removing user."""

    # user = User.query.get(user_id)
    # user.query.delete()

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect ('/users')




