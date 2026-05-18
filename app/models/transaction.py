# app/models/transaction.py
# Transaction database model.

from ..extensions import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Transaction {self.id} {self.amount}>'
