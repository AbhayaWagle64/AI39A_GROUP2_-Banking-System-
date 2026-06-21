from app.database import Database


class WalletModel:
    def __init__(self):
        self.table = "transactions"

    def create_transaction(self, sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status='completed'):
        db = Database()
        db.execute(
<<<<<<< HEAD
            "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
=======
            "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (%s, %s, %s, %s, %s, %s)",
>>>>>>> abhaya-wagle
            (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status)
        )
        db.close()

    def get_user_balance(self, username):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            "SELECT balance FROM register WHERE username = ?", (username,)
=======
            "SELECT balance FROM register WHERE username = %s", (username,)
>>>>>>> abhaya-wagle
        )
        db.close()
        if result:
            return float(result['balance']) if result['balance'] else 0.0
        return 0.0

    def update_user_balance(self, username, new_balance):
        db = Database()
        db.execute(
<<<<<<< HEAD
            "UPDATE register SET balance = ? WHERE username = ?",
=======
            "UPDATE register SET balance = %s WHERE username = %s",
>>>>>>> abhaya-wagle
            (str(new_balance), username)
        )
        db.close()

    def get_user_by_customer_id(self, customer_id):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            "SELECT username, email FROM register WHERE epaisa_id = ? OR phone = ? OR username = ? OR email = ?",
=======
            "SELECT username, email FROM register WHERE epaisa_id = %s OR phone = %s OR username = %s OR email = %s",
>>>>>>> abhaya-wagle
            (customer_id, customer_id, customer_id, customer_id)
        )
        db.close()
        return result

    def get_user_by_username(self, username):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            "SELECT * FROM register WHERE username = ?", (username,)
=======
            "SELECT * FROM register WHERE username = %s", (username,)
>>>>>>> abhaya-wagle
        )
        db.close()
        return result

    def get_all_transactions(self, username):
        db = Database()
        results = db.fetch_all(
<<<<<<< HEAD
            "SELECT * FROM transactions WHERE sender_email = (SELECT email FROM register WHERE username = ?) OR receiver_email = (SELECT email FROM register WHERE username = ?) ORDER BY transaction_date DESC",
=======
            "SELECT * FROM transactions WHERE sender_email = (SELECT email FROM register WHERE username = %s) OR receiver_email = (SELECT email FROM register WHERE username = %s) ORDER BY transaction_date DESC",
>>>>>>> abhaya-wagle
            (username, username)
        )
        db.close()
        return results

    def get_transaction_count(self, username):
        db = Database()
        result = db.fetch_one(
<<<<<<< HEAD
            "SELECT COUNT(*) AS total FROM transactions WHERE sender_email = (SELECT email FROM register WHERE username = ?) OR receiver_email = (SELECT email FROM register WHERE username = ?)",
=======
            "SELECT COUNT(*) AS total FROM transactions WHERE sender_email = (SELECT email FROM register WHERE username = %s) OR receiver_email = (SELECT email FROM register WHERE username = %s)",
>>>>>>> abhaya-wagle
            (username, username)
        )
        db.close()
        if result and result.get("total") is not None:
            return int(result["total"])
        return 0