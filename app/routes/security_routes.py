# app/routes/security_routes.py
# Routes for security pages.

from flask import Blueprint
from ..controllers.security_controller import (
    show_two_factor,
    show_security_question,
    show_login_activity,
    show_freeze_account,
    show_change_pin,
)

security_bp = Blueprint('security', __name__, url_prefix='/security')

security_bp.route('/two-factor', methods=['GET'])(show_two_factor)
security_bp.route('/security-question', methods=['GET'])(show_security_question)
security_bp.route('/login-activity', methods=['GET'])(show_login_activity)
security_bp.route('/freeze-account', methods=['GET'])(show_freeze_account)
security_bp.route('/change-pin', methods=['GET'])(show_change_pin)
