from sqlite3 import IntegrityError

from app.models.user import User
from app.security import Security
from app.database import get_connection


class AuthController:

    @staticmethod
    def register(
        name,
        phone,
        email,
        password
    ):

        if User.get_by_phone(phone):
            return {
                "success": False,
                "message": "Phone number already registered."
            }

        wallet_id = (
            Security.generate_wallet_id()
        )

        hashed_password = (
            Security.hash_password(password)
        )

        try:
            User.create(
                wallet_id,
                name,
                phone,
                email,
                hashed_password
            )
        except IntegrityError:
            return {
                "success": False,
                "message": "Phone number already registered."
            }

        return {
            "success": True,
            "wallet_id": wallet_id
        }

    @staticmethod
    def login(phone, password):

        user = User.get_by_phone(phone)

        if not user:

            return {
                "success": False,
                "message": "User not found. Please sign up first."
            }

        if user["account_locked"] == 1:

            return {
                "success": False,
                "message": "Account blocked."
            }

        if Security.verify_password(
            password,
            user["password"]
        ):

            conn = get_connection()

            conn.execute("""
            UPDATE users
            SET failed_attempts=0
            WHERE id=?
            """,
            (user["id"],))

            conn.commit()
            conn.close()

            return {
                "success": True,
                "message": "Login successful",
                "wallet_id": user["wallet_id"]
            }

        remaining = 3 - (
            user["failed_attempts"] + 1
        )

        conn = get_connection()

        if remaining <= 0:

            conn.execute("""
            UPDATE users
            SET account_locked=1
            WHERE id=?
            """,
            (user["id"],))

            conn.commit()

            conn.close()

            return {
                "success": False,
                "message": "Account blocked after 3 failed attempts."
            }

        conn.execute("""
        UPDATE users
        SET failed_attempts=
        failed_attempts+1
        WHERE id=?
        """,
        (user["id"],))

        conn.commit()

        conn.close()

        return {
            "success": False,
            "message":
            f"Invalid password. Attempts left: {remaining}"
        }