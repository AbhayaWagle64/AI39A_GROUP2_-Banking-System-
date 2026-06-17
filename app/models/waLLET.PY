from app.database import get_connection


class Wallet:

    @staticmethod
    def create(wallet_id, user_id):

        conn = get_connection()

        conn.execute("""
        INSERT INTO wallets(
        wallet_id,
        user_id,
        balance
        )
        VALUES(?,?,0)
        """,
        (
            wallet_id,
            user_id
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get(wallet_id):

        conn = get_connection()

        wallet = conn.execute(
            "SELECT * FROM wallets WHERE wallet_id=?",
            (wallet_id,)
        ).fetchone()

        conn.close()

        return wallet