# app/services/transaction_service.py
# Transaction service with simple operations.


def record_transaction(amount, description):
    return {'transaction_id': 1, 'amount': amount, 'description': description}
