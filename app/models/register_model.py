from werkzeug.security import generate_password_hash
from app.database import Database


class RegisterModel:
    def __init__(self):
        self.table = "register"

    def find_by_username(self, username):
        db = Database()
        result = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE username = %s", (username,)
        )
        db.close()
        return result

    def find_by_email(self, email):
        db = Database()
        result = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE email = %s", (email,)
        )
        db.close()
        return result

    def find_by_phone(self, phone):
        db = Database()
        result = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE phone = %s", (phone,)
        )
        db.close()
        return result

    def create(self, username, password, full_name, email, phone, address, account_type='Savings', date_joined='2026-01-01'):
        db = Database()
        db.execute(
            f"INSERT INTO {self.table} (username, password, full_name, email, phone, address, account_type, date_joined) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (username, generate_password_hash(password), full_name, email, phone, address, account_type, date_joined)
        )
        db.close()

    def delete(self, username):
        db = Database()
        db.execute(f"DELETE FROM {self.table} WHERE username = %s", (username,))
        db.close()
