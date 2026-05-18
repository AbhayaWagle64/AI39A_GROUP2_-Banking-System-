# app/utils/security.py
# Basic security helpers.

import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
