from app.routes.auth_routes import main as auth_bp
from app.routes.user_routes import main as user_bp
from app.routes.admin_routes import main as admin_bp
from app.routes.bill_payment_routes import main as bill_payment_bp
from app.routes.report_routes import report_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(bill_payment_bp)
    app.register_blueprint(report_bp)
