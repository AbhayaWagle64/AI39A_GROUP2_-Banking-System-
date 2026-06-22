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

    def find_by_epaisa_id(self, epaisa_id):
        db = Database()
        result = db.fetch_one(
            f"SELECT * FROM {self.table} WHERE epaisa_id = %s", (epaisa_id,)
        )
        db.close()
        return result

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
        )
        db.close()
        return epaisa_id

    def delete(self, username):
        db = Database()
        db.execute(f"DELETE FROM {self.table} WHERE username = %s", (username,))
        db.close()

    def update_password(self, username, password_hash):
        db = Database()
        db.execute(f"UPDATE {self.table} SET password = %s WHERE username = %s", (password_hash, username))
        db.close()
        return True
