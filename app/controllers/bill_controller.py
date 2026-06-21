from app.database import get_connection


class BillController:

    @staticmethod
    def pay_bill(user_id, bill_type, customer_id, amount):

        conn = get_connection()

        conn.execute("""
        CREATE TABLE IF NOT EXISTS bills(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bill_type TEXT,
            customer_id TEXT,
            amount REAL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.execute("""
        INSERT INTO bills(
            user_id,
            bill_type,
            customer_id,
            amount,
            status
        )
        VALUES(?,?,?,?,?)
        """,
        (
            user_id,
            bill_type,
            customer_id,
            amount,
            "PAID"
        ))

        conn.commit()
        conn.close()

        return True