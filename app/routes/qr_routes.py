from flask import Blueprint

from ..controllers.qr_controller import qr_payment, show_qr_payment

qr_bp = Blueprint("qr", __name__)

qr_bp.add_url_rule("/qr-payment", view_func=show_qr_payment)
qr_bp.add_url_rule("/qr/pay", methods=["POST"], view_func=qr_payment)
