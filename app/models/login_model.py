from werkzeug.security import generate_password_hash
from app.database import Database


class LoginModel:
    def __init__(self):
        self.table = "login"

    def find_by_username(self, username):
        db = Database()
        result = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE username = %s", (username,)
        )
        db.close()
        return result

    def create(self, username, password_hash, full_name):
        db = Database()
        existing = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE username = %s", (username,)
        )
        if existing:
            db.execute(
                f"UPDATE {self.table} SET password = %s, full_name = %s WHERE username = %s",
                (password_hash, full_name, username)
            )
        else:
            db.execute(
                f"INSERT INTO {self.table} (username, password, full_name) VALUES (%s, %s, %s)",
                (username, password_hash, full_name)
            )
        db.close()

    def delete(self, username):
        db = Database()
        db.execute(f"DELETE FROM {self.table} WHERE username = %s", (username,))
        db.close()
