from werkzeug.security import check_password_hash
from app.database import Database


class AdminModel:
    def __init__(self):
        self.table = "administration"

    def find_by_email(self, admin_email):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            f"SELECT * FROM {self.table} WHERE admin_email = ?", (admin_email,)
=======
            f"SELECT * FROM {self.table} WHERE admin_email = %s", (admin_email,)
>>>>>>> abhaya-wagle
        )
        db.close()
        return result

    def verify_password(self, admin_email, password):
        admin = self.find_by_email(admin_email)
        if admin and admin.get("password"):
            return check_password_hash(admin["password"], password)
        return False