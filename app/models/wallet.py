# app/models/wallet.py
# Wallet database model.

from ..extensions import db


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<Wallet user_id={self.user_id} balance={self.balance}>'
