# app/services/otp_service.py
# OTP generation service.

import random


def generate_otp():
    return str(random.randint(100000, 999999))
