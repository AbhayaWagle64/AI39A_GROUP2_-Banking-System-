from app.database import Database


class RechargeModel:

    def __init__(self):
        self.table = "recharges"


    def create(
        self,
        user_id,
        mobile_number,
        operator,
        amount,
        plan_description=None,
        transaction_id=None
    ):

        db = Database()

        db.execute(
            f"""
            INSERT INTO {self.table}
            (
                user_id,
                transaction_id,
                mobile_number,
                operator,
                amount,
                plan_description
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                user_id,
                transaction_id,
                mobile_number,
                operator,
                amount,
                plan_description
            )
        )

        db.close()

        return True



    def find_by_user(self, user_id):

        db = Database()

        result = db.fetch_all(
            f"""
            SELECT *
            FROM {self.table}
            WHERE user_id = %s
            """,
            (user_id,)
        )

        db.close()

        return result



    def find_by_id(self, recharge_id):

        db = Database()

        result = db.fetch_one(
            f"""
            SELECT *
            FROM {self.table}
            WHERE id = %s
            """,
            (recharge_id,)
        )

        db.close()

        return result