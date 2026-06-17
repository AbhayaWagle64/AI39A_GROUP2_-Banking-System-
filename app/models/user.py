from app.database import get_connection


class User:

    @staticmethod
    def create(
        wallet_id,
        name,
        phone,
        email,
        password
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(
        wallet_id,
        name,
        phone,
        email,
        password
        )
        VALUES(?,?,?,?,?)
        """,
        (
            wallet_id,
            name,
            phone,
            email,
            password
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_phone(phone):

        conn = get_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE phone=?",
            (phone,)
        ).fetchone()

        conn.close()

        return user