from app.database import get_connection


class WalletController:

    @staticmethod
    def get_dashboard(wallet_id):

        conn = get_connection()

        wallet = conn.execute("""
        SELECT *
        FROM wallets
        WHERE wallet_id=?
        """,
        (wallet_id,)
        ).fetchone()

        conn.close()

        return wallet