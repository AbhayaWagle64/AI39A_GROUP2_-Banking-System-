# app/forms/register_form.py
# Simple form object for user registration.

class RegisterForm:
    def __init__(self, data):
        self.username = data.get('username', '')
        self.email = data.get('email', '')
        self.password = data.get('password', '')

    def validate(self):
        return bool(self.username) and bool(self.email) and bool(self.password)
