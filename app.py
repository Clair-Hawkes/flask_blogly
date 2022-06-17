"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


############### User routes

@app.get('/')
def index():
    """Redirect to users route"""

    return redirect('/users')


@app.get('/users')
def user_list():
    """List users and show homepage."""

    users = User.query.order_by('id').all()
    return render_template("user_list.html", users=users)


@app.get('/users/new')
def user_add_page():
    """Show add user form with fields for first/last name and img url."""

    return render_template("user_add.html")


@app.post('/users/new')
def user_add():
    """Creates new user instance and commits to DB, from fields values.
    Redirects to /users page."""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['img-url']
    if not image_url:
        image_url = None

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

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).order_by('created_at').all()

    return render_template(
        'user_page.html',
        user=user,
        posts=posts)


@app.get('/users/<int:user_id>/edit')
def user_edit_page(user_id):
    """Show edit user page per user, with fields to update data."""

    user = User.query.get_or_404(user_id)

    if not user.image_url:
        user.image_url = ""

    return render_template('user_edit.html', user=user)


@app.post('/users/<int:user_id>/edit')
def user_edit(user_id):
    """Updates user instance and commits to DB, with fields values.
    Redirects to /users page."""

    user = User.query.get(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']
    if not user.image_url:
        user.image_url = None

    db.session.commit()

    return redirect('/users')


@app.post("/users/<int:user_id>/delete")
def user_delete(user_id):
    """Delete User commits update to DB removing user. Redirects to /users list"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')


############ Post routes

@app.get("/users/<int:user_id>/posts/new")
def post_add_page(user_id):
    """Delete User commits update to DB removing user. Redirects to /users list"""

    user = User.query.get_or_404(user_id)

    return render_template('post_add.html', user=user)

@app.post("/users/<int:user_id>/posts/new")
def post_add(user_id):
    """..."""

    #TODO: get_or_404 user to check id against
    title = request.form['title']
    content = request.form['content']
    #user.post.add(Post())
    post = Post(
        title=title,
        content=content,
        user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.get('/posts/<int:post_id>')
def post_page(post_id):
    """Show post title and content per post id"""

    post = Post.query.get_or_404(post_id)

    return render_template('post_page.html', post=post)

@app.get('/posts/<int:post_id>/edit')
def post_edit_page(post_id):
    """Show edit post page per user, with fields to update data."""

    post = Post.query.get_or_404(post_id)

    return render_template('post_edit.html', post=post)


@app.post('/posts/<int:post_id>/edit')
def post_edit(post_id):
    """Updates post instance and commits to DB, with fields values.
    Redirects to post page."""
    #TODO: or_404
    post = Post.query.get(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.post('/posts/<int:post_id>/delete')
def post_delete(post_id):
    """Delete post commits update to DB removing post.
    Redirects to user page"""
    #TODO: or_404
    post = Post.query.get(post_id)
    user_id = post.user.id

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')