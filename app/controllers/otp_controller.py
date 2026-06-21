import random

from datetime import datetime
from datetime import timedelta

from app.database import get_connection


class OTPController:

    @staticmethod
    def generate(transaction_id):

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        expiry = (
            datetime.now()
            + timedelta(minutes=5)
        )

        conn = get_connection()

        conn.execute("""
        INSERT INTO otp_verifications(
        transaction_id,
        otp_code,
        expires_at
        )
        VALUES(?,?,?)
        """,
        (
            transaction_id,
            otp,
            expiry
        ))

        conn.commit()
        conn.close()

        return otp

    @staticmethod
    def verify(transaction_id, otp):

        conn = get_connection()

        record = conn.execute("""
        SELECT *
        FROM otp_verifications
        WHERE transaction_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (transaction_id,)
        ).fetchone()

        conn.close()

        if not record:
            return False

        if record["otp_code"] != otp:
            return False

        expiry = datetime.fromisoformat(
            record["expires_at"]
        )

        if datetime.now() > expiry:
            return False

        return True