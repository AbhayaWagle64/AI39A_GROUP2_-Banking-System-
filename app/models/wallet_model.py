from app.database import Database


class WalletModel:
    def __init__(self):
        self.table = "transactions"

    def create_transaction(self, sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status='completed'):
        db = Database()
        db.execute(
            "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
            (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status)
        )
        db.close()

    def get_user_balance(self, username):
        db = Database()
        result = db.fetch_one(
            "SELECT balance FROM register WHERE username = ?", (username,)
        )
        db.close()
        if result:
            return float(result['balance']) if result['balance'] else 0.0
        return 0.0

    def update_user_balance(self, username, new_balance):
        db = Database()
        db.execute(
            "UPDATE register SET balance = ? WHERE username = ?",
            (str(new_balance), username)
        )
        db.close()

    def get_user_by_customer_id(self, customer_id):
        db = Database()
        result = db.fetch_one(
            "SELECT username, email FROM register WHERE epaisa_id = ? OR phone = ? OR username = ? OR email = ?",
            (customer_id, customer_id, customer_id, customer_id)
        )
        db.close()
        return result

    def get_user_by_username(self, username):
        db = Database()
        result = db.fetch_one(
            "SELECT * FROM register WHERE username = ?", (username,)
        )
        db.close()
        return result

    def get_all_transactions(self, username):
        db = Database()
        results = db.fetch_all(
            "SELECT * FROM transactions WHERE sender_email = (SELECT email FROM register WHERE username = ?) OR receiver_email = (SELECT email FROM register WHERE username = ?) ORDER BY transaction_date DESC",
            (username, username)
        )
        db.close()
        return results

    def get_transaction_count(self, username):
        db = Database()
        result = db.fetch_one(
            "SELECT COUNT(*) AS total FROM transactions WHERE sender_email = (SELECT email FROM register WHERE username = ?) OR receiver_email = (SELECT email FROM register WHERE username = ?)",
            (username, username)
        )
        db.close()
        if result and result.get("total") is not None:
            return int(result["total"])
        return 0