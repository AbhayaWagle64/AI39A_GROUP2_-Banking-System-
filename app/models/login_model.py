from werkzeug.security import generate_password_hash
from app.database import Database


class LoginModel:
    def __init__(self):
        self.table = "login"

    def find_by_username(self, username):
        db = Database()
        result = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE username = ?", (username,)
        )
        db.close()
        return result

    def create(self, username, password_hash, full_name, epaisa_id=None):
        db = Database()
        existing = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE username = ?", (username,)
        )
        if existing:
            if epaisa_id:
                db.execute(
                    f"UPDATE {self.table} SET password = ?, full_name = ?, epaisa_id = ? WHERE username = ?",
                    (password_hash, full_name, epaisa_id, username)
                )
            else:
                db.execute(
                    f"UPDATE {self.table} SET password = ?, full_name = ? WHERE username = ?",
                    (password_hash, full_name, username)
                )
        else:
            if epaisa_id:
                db.execute(
                    f"INSERT INTO {self.table} (username, password, full_name, epaisa_id) VALUES (?, ?, ?, ?)",
                    (username, password_hash, full_name, epaisa_id)
                )
            else:
                db.execute(
                    f"INSERT INTO {self.table} (username, password, full_name) VALUES (?, ?, ?)",
                    (username, password_hash, full_name)
                )
        db.close()

    def delete(self, username):
        db = Database()
        db.execute(f"DELETE FROM {self.table} WHERE username = ?", (username,))
        db.close()
