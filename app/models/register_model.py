from werkzeug.security import generate_password_hash
from app.database import Database


class RegisterModel:
    def __init__(self):
        self.table = "register"

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

    def find_by_email(self, email):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            f"SELECT * FROM {self.table} WHERE email = ?", (email,)
=======
            f"SELECT * FROM {self.table} WHERE email = %s", (email,)
>>>>>>> abhaya-wagle
        )
        db.close()
        return result

    def find_by_phone(self, phone):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            f"SELECT * FROM {self.table} WHERE phone = ?", (phone,)
=======
            f"SELECT * FROM {self.table} WHERE phone = %s", (phone,)
>>>>>>> abhaya-wagle
        )
        db.close()
        return result

    def find_by_epaisa_id(self, epaisa_id):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            f"SELECT * FROM {self.table} WHERE epaisa_id = ?", (epaisa_id,)
=======
            f"SELECT * FROM {self.table} WHERE epaisa_id = %s", (epaisa_id,)
>>>>>>> abhaya-wagle
        )
        db.close()
        return result

<<<<<<< HEAD
    def create(self, username, password, full_name, email, phone, address, account_type='Savings', date_joined='2026-01-01', epaisa_id=None, balance=0.0):
        db = Database()
        if not epaisa_id:
            # SQLite compatible approach - get all epaisa_ids and find max
            result = db.fetch_one(
                "SELECT epaisa_id FROM register WHERE epaisa_id LIKE 'eP-%' ORDER BY epaisa_id DESC LIMIT 1"
            )
            if result and result.get("epaisa_id"):
                try:
                    num = int(result["epaisa_id"].split("-")[1]) + 1
                except (ValueError, IndexError):
                    num = 1001
            else:
                num = 1001
            epaisa_id = f"eP-{num}"
        customer_id = f"SB-{phone}" if phone and phone.startswith("98") else f"SB-{10001}"
        db.execute(
            f"INSERT INTO {self.table} (username, password, full_name, email, phone, customer_id, epaisa_id, balance, address, account_type, date_joined) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (username, generate_password_hash(password), full_name, email, phone, customer_id, epaisa_id, balance, address, account_type, date_joined)
=======
    def create(self, username, password, full_name, email, phone, address, account_type='Savings', date_joined='2026-01-01', epaisa_id=None):
        db = Database()
        if not epaisa_id:
            result = db.fetch_one(
                "SELECT CAST(SUBSTRING_INDEX(epaisa_id, '-', -1) AS UNSIGNED) AS num FROM register WHERE epaisa_id REGEXP %s ORDER BY num DESC LIMIT 1",
                ("^eP-[0-9]+$",)
            )
            num = int(result["num"]) + 1 if result and result.get("num") else 1001
            epaisa_id = f"eP-{num}"
        customer_id = f"SB-{phone}" if phone and phone.startswith("98") else f"SB-{10001}"
        db.execute(
            f"INSERT INTO {self.table} (username, password, full_name, email, phone, customer_id, epaisa_id, address, account_type, date_joined) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (username, generate_password_hash(password), full_name, email, phone, customer_id, epaisa_id, address, account_type, date_joined)
>>>>>>> abhaya-wagle
        )
        db.close()
        return epaisa_id

    def delete(self, username):
        db = Database()
<<<<<<< HEAD
        db.execute(f"DELETE FROM {self.table} WHERE username = ?", (username,))
=======
        db.execute(f"DELETE FROM {self.table} WHERE username = %s", (username,))
>>>>>>> abhaya-wagle
        db.close()
