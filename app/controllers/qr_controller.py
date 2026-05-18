# app/controllers/qr_controller.py
# Controllers for QR payment and QR generation pages.

from flask import render_template


def show_qr_payment():
    return render_template('qr/qr_payment.html')


def show_generate_qr():
    return render_template('qr/generate_qr.html')


def show_scan_qr():
    return render_template('qr/scan_qr.html')
