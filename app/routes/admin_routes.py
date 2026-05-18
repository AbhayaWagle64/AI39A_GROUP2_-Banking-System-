# app/routes/admin_routes.py
# Routes for the admin section.

from flask import Blueprint
from ..controllers.admin_controller import (
    show_admin_dashboard,
    show_manage_users,
    show_manage_transaction,
    show_fraud_reports,
    show_system_logs,
    show_admin_settings,
    show_user_details,
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

admin_bp.route('/dashboard', methods=['GET'])(show_admin_dashboard)
admin_bp.route('/users', methods=['GET'])(show_manage_users)
admin_bp.route('/transactions', methods=['GET'])(show_manage_transaction)
admin_bp.route('/fraud-reports', methods=['GET'])(show_fraud_reports)
admin_bp.route('/system-logs', methods=['GET'])(show_system_logs)
admin_bp.route('/settings', methods=['GET'])(show_admin_settings)
admin_bp.route('/user-details', methods=['GET'])(show_user_details)
