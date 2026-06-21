from flask import Blueprint

from ..controllers.wallet_controller import (
    show_add_money,
    show_linked_accounts,
    show_wallet,
    show_wallet_summary,
    show_withdraw_money,
    send_money,
    receive_money,
)

wallet_bp = Blueprint("wallet", __name__)

wallet_bp.add_url_rule("/wallet", view_func=show_wallet)
wallet_bp.add_url_rule("/wallet/summary", view_func=show_wallet_summary)
wallet_bp.add_url_rule("/wallet/add", view_func=show_add_money)
wallet_bp.add_url_rule("/wallet/withdraw", view_func=show_withdraw_money)
wallet_bp.add_url_rule("/wallet/linked-accounts", view_func=show_linked_accounts)
wallet_bp.add_url_rule("/send-money", methods=["GET", "POST"], view_func=send_money)
wallet_bp.add_url_rule("/sendmoney", methods=["GET", "POST"], view_func=send_money)
wallet_bp.add_url_rule("/receive-money", methods=["GET", "POST"], view_func=receive_money)
