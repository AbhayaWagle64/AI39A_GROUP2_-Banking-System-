from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .wallet_routes import wallet_bp
from .transaction_routes import transaction_bp
from .user_routes import user_bp
from .qr_routes import qr_bp
from .report_routes import report_bp
from .notification_routes import notifications_bp
from .bill_payment_routes import bill_payment_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(bill_payment_bp)
    app.register_blueprint(admin_bp)
