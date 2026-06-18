from flask import Flask
from flask_mail import Mail

# Keep this here so it's created first!
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'epaisa123'

    # Email config (Gmail SMTP)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'kalyant413@gmail.com'
    app.config['MAIL_PASSWORD'] = 'hnmxntvmdcappwch'      
    app.config['MAIL_DEFAULT_SENDER'] = 'kalyant413@gmail.com' 

    mail.init_app(app)

    # --- ROUTE IMPORTS MOVED HERE ---
    # By placing these inside the function, mail is fully set up before these files load!
    from app.routes.auth import AuthRoutes
    from app.routes.wallet import WalletRoutes
    from app.routes.dashboard import DashboardRoutes
    from app.routes.password_reset import PasswordResetRoutes
    from app.routes.mini_statement import MiniStatementRoutes
    from app.routes.transaction_otp import TransactionOTPRoutes
    from app.routes.mobile_recharge import MobileRechargeRoutes

    # Register blueprints normally
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
    transaction_otp_routes = TransactionOTPRoutes()
    app.register_blueprint(transaction_otp_routes.register())
    mobile_recharge_routes = MobileRechargeRoutes()
    app.register_blueprint(mobile_recharge_routes.register())

    return app