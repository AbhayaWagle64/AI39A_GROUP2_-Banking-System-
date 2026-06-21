import unittest
from unittest.mock import MagicMock
from flask import Flask, session
from app.controllers.auth_controller import AuthController
from app.routes.auth_routes import allowed_file, validate_phone, validate_password


class TestBasicUtils(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'test-key'
        self.controller = AuthController()
        self.controller.login_model = MagicMock()
        self.controller.register_model = MagicMock()
        self.controller.wallet_model = MagicMock()

    def test_allowed_file(self):
        self.assertTrue(allowed_file('image.png'))
        self.assertTrue(allowed_file('photo.JPG'))
        self.assertFalse(allowed_file('document.pdf'))
        self.assertFalse(allowed_file('noext'))

    def test_validate_phone(self):
        self.assertTrue(validate_phone('9812345678'))
        self.assertFalse(validate_phone('12345'))
        self.assertFalse(validate_phone('98123456'))

    def test_validate_password(self):
        # valid: min 8, has uppercase, digit, special
        self.assertTrue(validate_password('Secret1!'))
        # too short
        self.assertFalse(validate_password('Ab1!'))
        # missing uppercase
        self.assertFalse(validate_password('secret1!'))
        # missing digit
        self.assertFalse(validate_password('Secret!!'))
        # missing special
        self.assertFalse(validate_password('Secret12'))

    def test_get_current_user_none_when_no_session(self):
        with self.app.test_request_context():
            # session empty
            self.assertIsNone(self.controller.get_current_user())

    def test_get_current_user_returns_expected(self):
        login_data = {'full_name': 'Bob', 'epaisa_id': 'eP-2001'}
        register_data = {
            'email': 'bob@example.com',
            'phone': '9812345678',
            'address': 'Somewhere',
            'account_type': 'Savings',
            'date_joined': '2026-01-01',
            'balance': '150.5',
            'epaisa_id': 'eP-2001'
        }
        self.controller.login_model.find_by_username.return_value = login_data
        self.controller.register_model.find_by_username.return_value = register_data
        self.controller.wallet_model.get_transaction_count.return_value = 3

        with self.app.test_request_context():
            session['user_id'] = 'bob'
            user = self.controller.get_current_user()
            self.assertIsNotNone(user)
            self.assertEqual(user['username'], 'bob')
            self.assertEqual(user['full_name'], 'Bob')
            self.assertEqual(user['email'], 'bob@example.com')
            self.assertEqual(user['phone'], '9812345678')
            self.assertEqual(user['balance'], 150.5)
            self.assertEqual(user['transaction_count'], 3)


if __name__ == '__main__':
    unittest.main()
