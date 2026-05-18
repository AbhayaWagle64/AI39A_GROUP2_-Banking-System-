# app/routes/dashboard_routes.py
# Routes for dashboard pages.

from flask import Blueprint
from ..controllers.dashboard_controller import (
    show_user_dashboard,
    show_dashboard,
    show_admin_dashboard,
    show_analytics,
)

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

dashboard_bp.route('/', methods=['GET'])(show_dashboard)
dashboard_bp.route('/user', methods=['GET'])(show_user_dashboard)
dashboard_bp.route('/admin', methods=['GET'])(show_admin_dashboard)
dashboard_bp.route('/analytics', methods=['GET'])(show_analytics)
