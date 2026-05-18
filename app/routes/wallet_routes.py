# app/routes/wallet_routes.py
# Routes for wallet management pages.

from flask import Blueprint
from ..controllers.wallet_controller import (
    show_wallet,
    show_wallet_summary,
    show_add_money,
    show_withdraw_money,
    show_linked_accounts,
)

wallet_bp = Blueprint('wallet', __name__, url_prefix='/wallet')

wallet_bp.route('/', methods=['GET'])(show_wallet)
wallet_bp.route('/summary', methods=['GET'])(show_wallet_summary)
wallet_bp.route('/add', methods=['GET'])(show_add_money)
wallet_bp.route('/withdraw', methods=['GET'])(show_withdraw_money)
wallet_bp.route('/linked-accounts', methods=['GET'])(show_linked_accounts)
