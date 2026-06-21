from app.database import Database


class RechargeStatusModel:

    def __init__(self):
        self.table = "recharges"



    def update_status(self, recharge_id, status):

        db = Database()


        db.execute(
            f"""
            UPDATE {self.table}
            SET status = %s
            WHERE id = %s
            """,
            (
                status,
                recharge_id
            )
        )


        db.close()

        return True



    def get_status(self, recharge_id):

        db = Database()


        result = db.fetch_one(
            f"""
            SELECT id, status, created_at
            FROM {self.table}
            WHERE id = %s
            """,
            (recharge_id,)
        )


        db.close()

        return result



    def get_successful_recharges(self):

        db = Database()


        result = db.fetch_all(
            f"""
            SELECT *
            FROM {self.table}
            WHERE status = 'success'
            """
        )


        db.close()

        return result



    def get_failed_recharges(self):

        db = Database()


        result = db.fetch_all(
            f"""
            SELECT *
            FROM {self.table}
            WHERE status = 'failed'
            """
        )


        db.close()

        return result