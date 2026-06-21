from flask import Blueprint

from ..controllers.notification_controller import notifications

notifications_bp = Blueprint("notification", __name__)

notifications_bp.add_url_rule("/notifications", view_func=notifications)
