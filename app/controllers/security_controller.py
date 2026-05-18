# app/controllers/security_controller.py
# Controllers for security and account safety pages.

from flask import render_template


def show_two_factor():
    return render_template('security/two_factor.html')


def show_security_question():
    return render_template('security/security_question.html')


def show_login_activity():
    return render_template('security/login_activity.html')


def show_freeze_account():
    return render_template('security/freeze_account.html')


def show_change_pin():
    return render_template('security/change_pin.html')
