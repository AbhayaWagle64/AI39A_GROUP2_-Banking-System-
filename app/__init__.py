from flask import Flask
from app.routes.auth import AuthRoutes
from app.routes.wallet import WalletRoutes
from app.routes.dashboard import DashboardRoutes
from app.routes.password_reset import PasswordResetRoutes
from app.routes.mini_statement import MiniStatementRoutes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'epaisa123'

    auth_routes = AuthRoutes()
    app.register_blueprint(auth_routes.register())

    wallet_routes = WalletRoutes()
    app.register_blueprint(wallet_routes.register())

    dashboard_routes = DashboardRoutes()
    app.register_blueprint(dashboard_routes.register())

    password_reset_routes = PasswordResetRoutes()
    app.register_blueprint(password_reset_routes.register())

    mini_statement_routes = MiniStatementRoutes()
    app.register_blueprint(mini_statement_routes.register())

    return app