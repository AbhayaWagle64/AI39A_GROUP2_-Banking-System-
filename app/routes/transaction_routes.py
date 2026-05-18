# app/routes/transaction_routes.py
# Routes for user transaction pages.

from flask import Blueprint
from ..controllers.transaction_controller import (
    show_transaction_history,
    show_send_money,
    show_receive_money,
    show_scheduled,
    show_refund,
    show_transaction_details,
)

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

transaction_bp.route('/', methods=['GET'])(show_transaction_history)
transaction_bp.route('/send', methods=['GET'])(show_send_money)
transaction_bp.route('/receive', methods=['GET'])(show_receive_money)
transaction_bp.route('/scheduled', methods=['GET'])(show_scheduled)
transaction_bp.route('/refund', methods=['GET'])(show_refund)
transaction_bp.route('/details', methods=['GET'])(show_transaction_details)
