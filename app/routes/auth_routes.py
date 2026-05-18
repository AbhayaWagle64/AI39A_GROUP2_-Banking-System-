# app/routes/auth_routes.py
# Routes for user authentication pages.

from flask import Blueprint
from ..controllers.auth_controller import (
    show_login,
    handle_login,
    show_register,
    show_forgot_password,
    show_reset_password,
    show_verify_otp,
    show_change_password,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_bp.route('/login', methods=['GET'])(show_login)
auth_bp.route('/login', methods=['POST'])(handle_login)
auth_bp.route('/register', methods=['GET'])(show_register)
auth_bp.route('/forgot-password', methods=['GET'])(show_forgot_password)
auth_bp.route('/reset-password', methods=['GET'])(show_reset_password)
auth_bp.route('/verify-otp', methods=['GET'])(show_verify_otp)
auth_bp.route('/change-password', methods=['GET'])(show_change_password)
