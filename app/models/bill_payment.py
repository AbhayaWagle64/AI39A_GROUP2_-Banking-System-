# app/models/bill_payment.py
# Bill payment model for billing records.

from ..extensions import db


class BillPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_type = db.Column(db.String(80))
    amount = db.Column(db.Float)

    def __repr__(self):
        return f'<BillPayment {self.bill_type} {self.amount}>'
