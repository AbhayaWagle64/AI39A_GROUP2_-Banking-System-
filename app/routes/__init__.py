# app/routes/__init__.py
# Register all blueprints for the application.

from .auth_routes import auth_bp
from .payment_routes import payment_bp
from .wallet_routes import wallet_bp
from .transaction_routes import transaction_bp
from .admin_routes import admin_bp
from .dashboard_routes import dashboard_bp
from .notification_routes import notifications_bp
from .profile_routes import profile_bp
from .bills_routes import bills_bp
from .qr_routes import qr_bp
from .security_routes import security_bp
from .home_routes import home_bp
from .api_routes import api_bp


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(bills_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(api_bp)
