from flask import Blueprint

from ..controllers.bill_payment_controller import bill_payment

bill_payment_bp = Blueprint("bill_payment", __name__)

bill_payment_bp.add_url_rule("/bill-payment", methods=["GET", "POST"], view_func=bill_payment)
