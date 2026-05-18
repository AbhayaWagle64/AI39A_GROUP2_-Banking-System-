# app/controllers/wallet_controller.py
# Wallet pages for adding, withdrawing, and viewing balance.

from flask import render_template


def show_wallet():
    return render_template('wallet/wallet.html')


def show_wallet_summary():
    return render_template('wallet/wallet_summary.html')


def show_add_money():
    return render_template('wallet/add_money.html')


def show_withdraw_money():
    return render_template('wallet/withdraw_money.html')


def show_linked_accounts():
    return render_template('wallet/linked_accounts.html')
