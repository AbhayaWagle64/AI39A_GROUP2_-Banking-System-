# app/routes/notification_routes.py
# Routes for notification pages.

from flask import Blueprint
from ..controllers.notification_controller import (
    show_notifications,
    show_notification_settings,
)

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

notifications_bp.route('/', methods=['GET'])(show_notifications)
notifications_bp.route('/settings', methods=['GET'])(show_notification_settings)
