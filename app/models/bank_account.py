# app/models/bank_account.py
# Bank account model for linked accounts.

from ..extensions import db


class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    bank_name = db.Column(db.String(120))

    def __repr__(self):
        return f'<BankAccount {self.bank_name}>'
