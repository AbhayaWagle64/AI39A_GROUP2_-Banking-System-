from app.database import Database

class AddWithdrawModel:
  def __init__(self):
    self.register_table = "register"
    self.transaction_table = "transactions"


def get_balance(self, username):

    db = Database()

    user = db.fetch_one(
        f"""
        SELECT balance
        FROM {self.register_table}
        WHERE username = %s
        """,
        (username,)
    )

    db.close()

    if user:
        return float(user["balance"])

    return 0.0


def add_money(self, username, amount):

    db = Database()

    try:

        amount = float(amount)

        if amount <= 0:
            db.close()
            return False, "Amount must be greater than zero."

        user = db.fetch_one(
            f"""
            SELECT balance, email, epaisa_id
            FROM {self.register_table}
            WHERE username = %s
            """,
            (username,)
        )

        if not user:
            db.close()
            return False, "User not found."

        new_balance = float(user["balance"]) + amount

        db.execute(
            f"""
            UPDATE {self.register_table}
            SET balance = %s
            WHERE username = %s
            """,
            (new_balance, username)
        )

        db.execute(
            f"""
            INSERT INTO {self.transaction_table}
            (
                sender_email,
                sender_epaisa_id,
                receiver_email,
                receiver_epaisa_id,
                amount,
                status
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                None,
                None,
                user["email"],
                user["epaisa_id"],
                amount,
                "add_money"
            )
        )

        db.close()

        return True, "Money added successfully."

    except Exception as e:

        db.close()

        return False, str(e)


def withdraw_money(self, username, amount):

    db = Database()

    try:

        amount = float(amount)

        if amount <= 0:
            db.close()
            return False, "Amount must be greater than zero."

        user = db.fetch_one(
            f"""
            SELECT balance, email, epaisa_id
            FROM {self.register_table}
            WHERE username = %s
            """,
            (username,)
        )

        if not user:
            db.close()
            return False, "User not found."

        current_balance = float(user["balance"])

        if current_balance < amount:
            db.close()
            return False, "Insufficient balance."

        new_balance = current_balance - amount

        db.execute(
            f"""
            UPDATE {self.register_table}
            SET balance = %s
            WHERE username = %s
            """,
            (new_balance, username)
        )

        db.execute(
            f"""
            INSERT INTO {self.transaction_table}
            (
                sender_email,
                sender_epaisa_id,
                receiver_email,
                receiver_epaisa_id,
                amount,
                status
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                user["email"],
                user["epaisa_id"],
                None,
                None,
                amount,
                "withdraw"
            )
        )

        db.close()

        return True, "Withdrawal successful."

    except Exception as e:

        db.close()

        return False, str(e)

