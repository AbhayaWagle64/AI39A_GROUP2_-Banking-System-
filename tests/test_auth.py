import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, Blueprint, session, get_flashed_messages
from app.controllers.auth_controller import AuthController
from app.auth import login_required


def make_test_app():
    app = Flask(__name__)
    app.secret_key = "test-secret-key"

    bp = Blueprint("auth", __name__)
    bp.route("/login", endpoint="login")(lambda: "login")
    app.register_blueprint(bp)

    user_bp = Blueprint("user", __name__)
    user_bp.route("/wallet", endpoint="wallet")(lambda: "wallet")
    app.register_blueprint(user_bp)
    return app


class TestAuthController(unittest.TestCase):
    def setUp(self):
        self.app = make_test_app()
        self.controller = AuthController()
        self.controller.register_model = MagicMock()
        self.controller.login_model = MagicMock()

    @patch("app.controllers.auth_controller.render_template")
    def test_register_get_shows_form(self, mock_render):
        mock_render.return_value = "register_page"
        with self.app.test_request_context(method="GET"):
            result = self.controller.register()
            self.assertEqual(result, "register_page")
            mock_render.assert_called_once_with("register.html")

    @patch("app.controllers.auth_controller.render_template")
    def test_register_missing_email_or_password_is_rejected(self, mock_render):
        mock_render.return_value = "register_page"
        with self.app.test_request_context(
            method="POST",
            data={"fullname": "", "email": "", "phone": "", "password": "", "confirm_password": ""},
        ):
            result = self.controller.register()
            self.assertEqual(result, "register_page")
            self.assertIn(("danger", "Email and password are required."), get_flashed_messages(with_categories=True))
            self.controller.register_model.create.assert_not_called()

    @patch("app.controllers.auth_controller.render_template")
    def test_register_invalid_phone_is_rejected(self, mock_render):
        mock_render.return_value = "register_page"
        with self.app.test_request_context(
            method="POST",
            data={"fullname": "Bob", "email": "bob@example.com", "phone": "12345", "password": "Secret1!", "confirm_password": "Secret1!"},
        ):
            result = self.controller.register()
            self.assertEqual(result, "register_page")
            self.assertIn(
                ("danger", "Phone number must be exactly 10 digits starting with 98 (e.g. 9812345678)."),
                get_flashed_messages(with_categories=True),
            )
            self.controller.register_model.create.assert_not_called()

    def test_register_duplicate_email_is_rejected(self):
        self.controller.register_model.find_by_email.return_value = {"email": "taken@example.com"}
        self.controller.register_model.find_by_username.return_value = None

        with self.app.test_request_context(
            method="POST",
            data={
                "fullname": "Bob",
                "email": "taken@example.com",
                "phone": "9812345678",
                "password": "Secret1!",
                "confirm_password": "Secret1!",
            },
        ):
            with patch("app.controllers.auth_controller.render_template") as mock_render:
                mock_render.return_value = "register_page"
                response = self.controller.register()
                self.assertEqual(response, "register_page")
                self.assertIn(("danger", "An account with this email already exists."), get_flashed_messages(with_categories=True))
            self.controller.register_model.create.assert_not_called()

    def test_register_success_saves_user_and_redirects(self):
        self.controller.register_model.find_by_email.return_value = None
        self.controller.register_model.find_by_username.return_value = None
        self.controller.register_model.find_by_phone.return_value = None

        with self.app.test_request_context(
            method="POST",
            data={
                "fullname": "Alice",
                "email": "alice@example.com",
                "phone": "9812345678",
                "password": "Secret1!",
                "confirm_password": "Secret1!",
            },
        ):
            response = self.controller.register()
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login", response.location)
            self.controller.register_model.create.assert_called_once()
            self.assertIn(("success", "Registration successful! Please login."), get_flashed_messages(with_categories=True))

    @patch("app.controllers.auth_controller.render_template")
    def test_register_invalid_email_is_rejected(self, mock_render):
        """An email without '@' should be rejected."""
        mock_render.return_value = "register_page"
        self.controller.register_model.find_by_email.return_value = None
        self.controller.register_model.find_by_username.return_value = None
        with self.app.test_request_context(
            method="POST",
            data={
                "fullname": "Charlie",
                "email": "charlieexample.com",  # invalid
                "phone": "9812345678",
                "password": "Secret1!",
                "confirm_password": "Secret1!",
            },
        ):
            result = self.controller.register()
            self.assertEqual(result, "register_page")
            self.assertIn(("danger", "Please enter a valid email address."), get_flashed_messages(with_categories=True))

    @patch("app.controllers.auth_controller.render_template")
    def test_register_password_mismatch_is_rejected(self, mock_render):
        """Mismatched password and confirmation should be rejected."""
        mock_render.return_value = "register_page"
        self.controller.register_model.find_by_email.return_value = None
        self.controller.register_model.find_by_username.return_value = None
        with self.app.test_request_context(
            method="POST",
            data={
                "fullname": "Dana",
                "email": "dana@example.com",
                "phone": "9812345678",
                "password": "Secret1!",
                "confirm_password": "Different1!",
            },
        ):
            result = self.controller.register()
            self.assertEqual(result, "register_page")
            self.assertIn(("danger", "Passwords do not match."), get_flashed_messages(with_categories=True))

    @patch("app.controllers.auth_controller.render_template")
    def test_register_short_or_weak_password_is_rejected(self, mock_render):
        """Passwords that don't meet complexity requirements are rejected."""
        mock_render.return_value = "register_page"
        self.controller.register_model.find_by_email.return_value = None
        self.controller.register_model.find_by_username.return_value = None
        with self.app.test_request_context(
            method="POST",
            data={
                "fullname": "Eve",
                "email": "eve@example.com",
                "phone": "9812345678",
                "password": "Ab1!",  # too short and weak
                "confirm_password": "Ab1!",
            },
        ):
            result = self.controller.register()
            self.assertEqual(result, "register_page")
            self.assertIn(("danger", "Password must be at least 8 characters with 1 uppercase letter, 1 number, and 1 special character."), get_flashed_messages(with_categories=True))

    @patch("app.controllers.auth_controller.render_template")
    def test_login_get_shows_form(self, mock_render):
        mock_render.return_value = "login_page"
        with self.app.test_request_context(method="GET"):
            result = self.controller.login()
            self.assertEqual(result, "login_page")
            mock_render.assert_called_once_with("login.html")

    @patch("app.controllers.auth_controller.render_template")
    def test_login_missing_fields_is_rejected(self, mock_render):
        mock_render.return_value = "login_page"
        with self.app.test_request_context(
            method="POST",
            data={"username": "", "password": ""},
        ):
            result = self.controller.login()
            self.assertEqual(result, "login_page")
            self.assertIn(("danger", "Username/email and password are required."), get_flashed_messages(with_categories=True))

    @patch("app.controllers.auth_controller.check_password_hash")
    @patch("app.controllers.auth_controller.render_template")
    def test_login_wrong_password_is_rejected(self, mock_render, mock_check_password):
        mock_render.return_value = "login_page"
        self.controller.login_model.find_by_username.return_value = {
            "username": "bob",
            "password": "hashed",
            "full_name": "Bob",
        }
        self.controller.register_model.find_by_username.return_value = {
            "username": "bob",
            "password": "hashed",
            "full_name": "Bob",
            "epaisa_id": "eP-1001",
        }
        mock_check_password.return_value = False

        with self.app.test_request_context(
            method="POST",
            data={"username": "bob", "password": "wrongpass"},
        ):
            result = self.controller.login()
            self.assertEqual(result, "login_page")
            self.assertIn(("danger", "Wrong username or password."), get_flashed_messages(with_categories=True))
            self.assertNotIn("user_id", session)

    @patch("app.controllers.auth_controller.check_password_hash")
    def test_login_success_sets_session_and_redirects(self, mock_check_password):
        self.controller.login_model.find_by_username.return_value = {
            "username": "bob",
            "password": "hashed",
            "full_name": "Bob",
        }
        self.controller.register_model.find_by_username.return_value = {
            "username": "bob",
            "password": "hashed",
            "full_name": "Bob",
            "epaisa_id": "eP-1001",
        }
        mock_check_password.return_value = True

        with self.app.test_request_context(
            method="POST",
            data={"username": "bob", "password": "Secret1!"},
        ):
            response = self.controller.login()
            self.assertEqual(session["user_id"], "bob")
            self.assertEqual(response.status_code, 302)
            self.assertIn("/wallet", response.location)
            self.assertIn(("success", "Login successful!"), get_flashed_messages(with_categories=True))

    def test_logout_clears_session_and_redirects(self):
        self.controller.login_model.delete = MagicMock()
        with self.app.test_request_context(method="GET"):
            session["user_id"] = "bob"
            response = self.controller.logout()
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login", response.location)
            self.assertNotIn("user_id", session)
            self.assertIn(("success", "Logged out successfully."), get_flashed_messages(with_categories=True))
            self.controller.login_model.delete.assert_called_once_with("bob")


class TestLoginRequiredDecorator(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "test-secret-key"
        auth = Blueprint("auth", __name__)

        @auth.route("/login")
        def login():
            return "login page"

        @auth.route("/home")
        @login_required
        def home():
            return "home page"

        self.app.register_blueprint(auth)
        self.client = self.app.test_client()

    def test_guest_redirects_to_login(self):
        response = self.client.get("/home")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_logged_in_user_can_access_page(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = "bob"

        response = self.client.get("/home")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "home page")


if __name__ == "__main__":
    unittest.main()
