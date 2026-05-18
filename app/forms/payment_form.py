# app/forms/payment_form.py
# Simple form object for payments.

class PaymentForm:
    def __init__(self, data):
        self.amount = data.get('amount', '')
        self.recipient = data.get('recipient', '')

    def validate(self):
        return bool(self.amount) and bool(self.recipient)
