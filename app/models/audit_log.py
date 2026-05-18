# app/models/audit_log.py
# Simple audit log model.

from ..extensions import db


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    timestamp = db.Column(db.String(100))

    def __repr__(self):
        return f'<AuditLog {self.action}>'
