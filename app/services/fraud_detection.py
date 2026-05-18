# app/services/fraud_detection.py
# Fraud detection helper with demo logic.


def is_transaction_suspicious(amount):
    return amount > 10000
