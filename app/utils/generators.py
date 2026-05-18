# app/utils/generators.py
# Random generator helpers.

import uuid


def generate_id():
    return str(uuid.uuid4())
