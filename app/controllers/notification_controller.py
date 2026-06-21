from app.database import get_connection


class NotificationController:

    @staticmethod
    def create(
        wallet_id,
        title,
        message
    ):

        conn = get_connection()

        conn.execute("""
        INSERT INTO notifications(
        wallet_id,
        title,
        message
        )
        VALUES(?,?,?)
        """,
        (
            wallet_id,
            title,
            message
        ))

        conn.commit()
        conn.close()