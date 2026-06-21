from flask import Blueprint

from ..controllers.report_controller import reports, report_wrong_transaction

report_bp = Blueprint("report", __name__)

report_bp.add_url_rule("/reports", view_func=reports)
report_bp.add_url_rule("/report-wrong-transaction", methods=["GET", "POST"], view_func=report_wrong_transaction)
