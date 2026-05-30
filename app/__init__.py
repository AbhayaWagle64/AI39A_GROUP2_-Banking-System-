from flask import Flask
from app.routes.auth import AuthRoutes
from app.routes.wallet import WalletRoutes  # ← ADD THIS LINE
from app.routes.dashboard import DashboardRoutes    # ADD THIS


def create_app():
    app = Flask(__name__)
    app.secret_key = 'epaisa123'

    auth_routes = AuthRoutes()
    app.register_blueprint(auth_routes.register())

    wallet_routes = WalletRoutes()                    # ← ADD THIS LINE
    app.register_blueprint(wallet_routes.register())  # ← ADD THIS LINE

    dashboard_routes = DashboardRoutes()                      # ADD THIS
    app.register_blueprint(dashboard_routes.register())       # ADD THIS

    return app