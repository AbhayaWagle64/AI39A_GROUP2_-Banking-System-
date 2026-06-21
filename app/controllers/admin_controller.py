from app.database import get_connection


class AdminController:

    @staticmethod
    def get_all_transactions():

        conn = get_connection()

        data = conn.execute("""
        SELECT * FROM transactions
        ORDER BY created_at DESC
        """).fetchall()

        conn.close()

        return data