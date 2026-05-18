# app/controllers/transaction_controller.py
# Transaction and transfer pages for users.

from flask import render_template


def show_transaction_history():
    return render_template('user_transactions/transaction_history.html')


def show_send_money():
    return render_template('user_transactions/send_money.html')


def show_receive_money():
    return render_template('user_transactions/receive_money.html')


def show_scheduled():
    return render_template('user_transactions/scheduled.html')


def show_refund():
    return render_template('user_transactions/refund.html')


def show_transaction_details():
    return render_template('user_transactions/transaction_details.html')
