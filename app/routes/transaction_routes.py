from flask import Blueprint

from app.controllers.transaction_confirmation_controller import TransactionController

transaction_bp = Blueprint("transaction", __name__)

transaction_bp.add_url_rule("/transactions", view_func=TransactionController.transaction_history)
transaction_bp.add_url_rule("/transactions/<int:transaction_id>", view_func=TransactionController.transaction_details)
