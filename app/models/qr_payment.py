# app/models/qr_payment.py
# QR payment model for QR code transactions.

from ..extensions import db


class QRPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_code = db.Column(db.String(255))
    amount = db.Column(db.Float)

    def __repr__(self):
        return f'<QRPayment {self.qr_code}>'
