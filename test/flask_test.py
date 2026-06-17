import unittest
from flask import Flask, Blueprint
from run.auth import login_required
class TestFlaskBase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key ='test_secret_key' 
        auth=Blueprint('auth', __name__)

        @auth.route("/login")
        def login():
            return "Login Page"
        
        @auth.route("/home")
        @login_required
        def home():
            return "Home Page"

        self.app.register_blueprint(auth)
        self.client = self.app.test_client()

        
def test_login_page(self):
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login Page', response.data)
def test_home_page_without_login(self):
            response = self.client.get('/home')
            self.assertEqual(response.status_code, 302)  # Should redirect to login
            self.assertIn('/login', response.headers['Location'])

def test_locked_page_redirects_a_guest(self):
    response = self.client.get('/home')
    self.assertEqual(response.status_code, 302)  # Should redirect to login
    self.assertIn('/login', response.headers['Location'])


def test_locked_page_redirects_for_logged_in_user(self):
    with self.client.session_transaction() as session:
        session['user_id'] = 1  # Simulate a logged-in user
    response = self.client.get('/home')
    self.assertEqual(response.status_code, 200)  # Should access home page
    self.assertIn(b'Home Page', response.data)

if __name__ == "__main__":
    unittest.main()