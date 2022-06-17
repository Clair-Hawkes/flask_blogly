from unittest import TestCase

from app import app, db
from models import User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None)

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_user_list(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("user_list", html)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_user_add_page(self):
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("user_add page", html)
            self.assertIn("<form", html)

    def test_user_page(self):
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("user_page", html)
            self.assertIn("<a href=", html)

            # Testing for 404 error with out of bounds user id.
            resp = c.get(f"/users/100001010101010")
            self.assertEqual(resp.status_code, 404)

    def test_user_edit_page(self):
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("user_edit page", html)
            self.assertIn("<input name=", html)

            # Testing for 404 error with out of bounds user id.
            resp = c.get(f"/users/100001010101010/edit")
            self.assertEqual(resp.status_code, 404)


class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data for user and posts."""

        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None)

        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id

        test_post = Post(
            title="test_title",
            content="test_content",
            user_id=test_user.id)

        test_post_two = Post(
            title="test_title_two",
            content="test_content_two",
            user_id=self.user_id)

        db.session.add_all([test_post, test_post_two])
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_post_page(self):
        """Check if post page loads correctly."""
        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("post_page", html)

    def test_post_edit_page(self):
        """Check if post edit page loads correctly."""
        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("post_edit", html)
            self.assertIn("<form", html)

            # Testing for 404 error with out of bounds user id.
            resp = c.get(f"/posts/8675309/edit")
            self.assertEqual(resp.status_code, 404)

    def test_post_edit_page(self):
        """Check if post edit changes are correctly stored in db, and displayed
            on redirected post page."""
        with self.client as c:
            resp = c.post(
                f"/posts/{self.post_id}/edit",
                data={
                    "title": "Hi Joel",
                    "content": "Coding is hard!"
                },
                follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hi Joel", html)
            self.assertIn("post_page", html)

    def test_post_delete(self):
        """Check if delete post view successfully redirects to user page."""
        with self.client as c:
            resp = c.post(
                f"/posts/{self.post_id}/delete",
                follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)
            self.assertIn("user_page", html)
