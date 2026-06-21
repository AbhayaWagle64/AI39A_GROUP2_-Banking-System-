from app.database import Database


class SavedPaymentModel:

    def __init__(self):
        self.table = "saved_payments"


    def create(
        self,
        user_id,
        recipient_name,
        recipient_email=None,
        recipient_phone=None,
        nickname=None,
        payment_type="wallet_transfer"
    ):

        db = Database()

        db.execute(
            f"""
            INSERT INTO {self.table}
            (
                user_id,
                recipient_name,
                recipient_email,
                recipient_phone,
                nickname,
                payment_type
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                user_id,
                recipient_name,
                recipient_email,
                recipient_phone,
                nickname,
                payment_type
            )
        )

        db.close()


    def find_by_user(self, user_id):

        db = Database()

        result = db.fetch_all(
            f"""
            SELECT *
            FROM {self.table}
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        db.close()

        return result


    def find_by_id(self, payment_id):

        db = Database()

        result = db.fetch_one(
            f"""
            SELECT *
            FROM {self.table}
            WHERE id = %s
            """,
            (payment_id,)
        )

        db.close()

        return result


    def delete(self, payment_id):

        db = Database()

        db.execute(
            f"""
            DELETE FROM {self.table}
            WHERE id = %s
            """,
            (payment_id,)
        )

        db.close()