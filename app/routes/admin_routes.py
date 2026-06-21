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

admin_bp = Blueprint("admin", __name__)

admin_bp.add_url_rule("/admin/dashboard", view_func=show_admin_dashboard)
admin_bp.add_url_rule("/admin/users", view_func=show_manage_users)
admin_bp.add_url_rule("/admin/transactions", view_func=show_manage_transaction)
admin_bp.add_url_rule("/admin/fraud-reports", view_func=show_fraud_reports)
admin_bp.add_url_rule("/admin/system-logs", view_func=show_system_logs)
admin_bp.add_url_rule("/admin/settings", view_func=show_admin_settings)
admin_bp.add_url_rule("/admin/user-details", view_func=show_user_details)
