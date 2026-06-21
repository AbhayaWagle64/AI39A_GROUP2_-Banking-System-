import random
from datetime import datetime, timedelta

from app.database import get_connection


otp_store = {}


class PasswordController:

    @staticmethod
    def request_reset(phone):

        otp = str(random.randint(100000, 999999))
        expiry = datetime.now() + timedelta(minutes=5)

        conn = get_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE phone=?",
            (phone,)
        ).fetchone()

        if not user:
            return {"success": False, "message": "User not found"}

        otp_store[phone] = {
            "otp": otp,
            "expiry": expiry
        }

        return {
            "success": True,
            "otp": otp  # simulate SMS/email
        }

    @staticmethod
    def verify_reset(phone, otp):

        if phone not in otp_store:
            return False

        data = otp_store[phone]

        if datetime.now() > data["expiry"]:
            return False

        return data["otp"] == otp