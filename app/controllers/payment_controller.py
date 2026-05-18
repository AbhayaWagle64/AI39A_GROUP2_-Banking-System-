# app/controllers/payment_controller.py
# Pages for payment flows and payment result screens.

from flask import render_template


def show_make_payment():
    return render_template('payment/make_payment.html')


def show_merchant_payment():
    return render_template('payment/merchant_payment.html')


def show_payment_success():
    return render_template('payment/payment_success.html')


def show_payment_failed():
    return render_template('payment/payment_failed.html')


def show_payment_receipt():
    return render_template('payment/payment_receipt.html')
