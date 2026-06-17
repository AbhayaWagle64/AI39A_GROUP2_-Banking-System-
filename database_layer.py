"""
E-Paisa Database Layer
Location: E:\practice\e-paisa\database_layer.py
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    wallet_balance = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Sprint 5: User Management fields
    is_banned = db.Column(db.Boolean, default=False)
    banned_at = db.Column(db.DateTime)
    ban_reason = db.Column(db.String(200))

    # Relationship to disputes
    disputes = db.relationship('Dispute', backref='user', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    tx_type = db.Column(db.String(20))  # credit or debit
    txn_type = db.Column(db.String(20))  # credit or debit (alias)
    amount = db.Column(db.Float, nullable=False)
    running_balance = db.Column(db.Float)
    status = db.Column(db.String(20), default='success')
    txn_status = db.Column(db.String(20), default='success')
    reference = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    recipient = db.Column(db.String(100))
    date = db.Column(db.DateTime)

class Dispute(db.Model):
    __tablename__ = 'disputes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    txn_id = db.Column(db.String(50), nullable=False)
    issue_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    resolution = db.Column(db.String(50), default='investigation')
    status = db.Column(db.String(20), default='open')
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = db.Column(db.DateTime)