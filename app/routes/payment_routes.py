# app/routes/payment_routes.py
# Routes for payment pages.

from flask import Blueprint
from ..controllers.payment_controller import (
    show_make_payment,
    show_merchant_payment,
    show_payment_success,
    show_payment_failed,
    show_payment_receipt,
)

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

payment_bp.route('/make', methods=['GET'])(show_make_payment)
payment_bp.route('/merchant', methods=['GET'])(show_merchant_payment)
payment_bp.route('/success', methods=['GET'])(show_payment_success)
payment_bp.route('/failed', methods=['GET'])(show_payment_failed)
payment_bp.route('/receipt', methods=['GET'])(show_payment_receipt)
