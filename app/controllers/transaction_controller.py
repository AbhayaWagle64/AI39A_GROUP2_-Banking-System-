from app.database import get_connection

from app.controllers.notification_controller import NotificationController


class TransactionController:

    TRANSACTION_FEE = 5

    @staticmethod
    def create(
        sender_wallet,
        receiver_wallet,
        amount
    ):

        conn = get_connection()

        receiver = conn.execute("""
        SELECT *
        FROM wallets
        WHERE wallet_id=?
        """,
        (receiver_wallet,)
        ).fetchone()

        if not receiver:

            conn.close()

            return {
                "success": False,
                "message":
                "Receiver wallet not found"
            }

        if receiver["status"] != "ACTIVE":

            conn.close()

            return {
                "success": False,
                "message":
                "Receiver account is frozen or closed"
            }

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO transactions(
        sender_wallet,
        receiver_wallet,
        amount,
        fee,
        status
        )
        VALUES(?,?,?,?,?)
        """,
        (
            sender_wallet,
            receiver_wallet,
            amount,
            5,
            "PENDING"
        ))

        transaction_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return {
            "success": True,
            "transaction_id":
            transaction_id
        }

    @staticmethod
    def complete(transaction_id):

        conn = get_connection()

        txn = conn.execute("""
        SELECT *
        FROM transactions
        WHERE id=?
        """,
        (transaction_id,)
        ).fetchone()

        receiver_wallet = txn["receiver_wallet"]

        amount = txn["amount"]

        conn.execute("""
        UPDATE wallets
        SET balance=
        balance + ?
        WHERE wallet_id=?
        """,
        (
            amount,
            receiver_wallet
        ))

        conn.execute("""
        UPDATE transactions
        SET status='SUCCESS'
        WHERE id=?
        """,
        (transaction_id,)
        )

        conn.commit()
        conn.close()

        NotificationController.create(
            receiver_wallet,
            "Money Received",
            f"You received Rs.{amount}"
        )