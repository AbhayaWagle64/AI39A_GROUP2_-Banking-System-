from werkzeug.security import generate_password_hash
from app.database import Database


class LoginModel:
    def __init__(self):
        self.table = "login"

    def find_by_username(self, username):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            f"SELECT * FROM {self.table} WHERE username = ?", (username,)
=======
            f"SELECT * FROM {self.table} WHERE username = %s", (username,)
>>>>>>> abhaya-wagle
        )
        db.close()
        return result

    def create(self, username, password_hash, full_name, epaisa_id=None):
        db = Database()
        existing = db.fetch_one(
<<<<<<< HEAD
            f"SELECT * FROM {self.table} WHERE username = ?", (username,)
=======
            f"SELECT * FROM {self.table} WHERE username = %s", (username,)
>>>>>>> abhaya-wagle
        )
        if existing:
            if epaisa_id:
                db.execute(
<<<<<<< HEAD
                    f"UPDATE {self.table} SET password = ?, full_name = ?, epaisa_id = ? WHERE username = ?",
=======
                    f"UPDATE {self.table} SET password = %s, full_name = %s, epaisa_id = %s WHERE username = %s",
>>>>>>> abhaya-wagle
                    (password_hash, full_name, epaisa_id, username)
                )
            else:
                db.execute(
<<<<<<< HEAD
                    f"UPDATE {self.table} SET password = ?, full_name = ? WHERE username = ?",
=======
                    f"UPDATE {self.table} SET password = %s, full_name = %s WHERE username = %s",
>>>>>>> abhaya-wagle
                    (password_hash, full_name, username)
                )
        else:
            if epaisa_id:
                db.execute(
<<<<<<< HEAD
                    f"INSERT INTO {self.table} (username, password, full_name, epaisa_id) VALUES (?, ?, ?, ?)",
=======
                    f"INSERT INTO {self.table} (username, password, full_name, epaisa_id) VALUES (%s, %s, %s, %s)",
>>>>>>> abhaya-wagle
                    (username, password_hash, full_name, epaisa_id)
                )
            else:
                db.execute(
<<<<<<< HEAD
                    f"INSERT INTO {self.table} (username, password, full_name) VALUES (?, ?, ?)",
=======
                    f"INSERT INTO {self.table} (username, password, full_name) VALUES (%s, %s, %s)",
>>>>>>> abhaya-wagle
                    (username, password_hash, full_name)
                )
        db.close()

    def delete(self, username):
        db = Database()
<<<<<<< HEAD
        db.execute(f"DELETE FROM {self.table} WHERE username = ?", (username,))
=======
        db.execute(f"DELETE FROM {self.table} WHERE username = %s", (username,))
>>>>>>> abhaya-wagle
        db.close()
