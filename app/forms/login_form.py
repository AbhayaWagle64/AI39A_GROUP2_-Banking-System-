# app/forms/login_form.py
# Simple form object for login pages.

class LoginForm:
    def __init__(self, data):
        self.username = data.get('username', '')
        self.password = data.get('password', '')

    def validate(self):
        return bool(self.username) and bool(self.password)
