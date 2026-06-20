from app.database import Database


class ProfileManagementModel:

    def __init__(self):
        self.table = "profile_management"


    def get_profile(self, username):

        db = Database()

        result = db.fetch_one(
            f"""
            SELECT *
            FROM {self.table}
            WHERE username = %s
            """,
            (username,)
        )

        db.close()

        return result


    def update_profile(
        self,
        username,
        full_name,
        email,
        phone,
        address
    ):

        db = Database()

        db.execute(
            f"""
            UPDATE {self.table}
            SET
                full_name = %s,
                email = %s,
                phone = %s,
                address = %s
            WHERE username = %s
            """,
            (
                full_name,
                email,
                phone,
                address,
                username
            )
        )

        db.close()


    def create_profile(
        self,
        username,
        full_name,
        email,
        phone,
        address,
        account_type
    ):

        db = Database()

        db.execute(
            f"""
            INSERT INTO {self.table}
            (
                username,
                full_name,
                email,
                phone,
                address,
                account_type
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                username,
                full_name,
                email,
                phone,
                address,
                account_type
            )
        )

        db.close()