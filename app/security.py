import hashlib
import secrets


class Security:

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    @staticmethod
    def verify_password(password, hashed):
        return (
            Security.hash_password(password)
            == hashed
        )

    @staticmethod
    def generate_wallet_id():
        return "EP" + secrets.token_hex(4).upper()