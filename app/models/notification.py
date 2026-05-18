# app/models/notification.py
# Notification model for user alerts.

from ..extensions import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(255))

    def __repr__(self):
        return f'<Notification {self.message}>'
