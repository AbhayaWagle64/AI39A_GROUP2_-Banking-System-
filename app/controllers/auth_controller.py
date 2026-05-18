# app/controllers/auth_controller.py
# Controllers for auth pages and login flows.

from flask import render_template, request, redirect, url_for, flash
from ..auth import check_username_password


def show_login():
    return render_template('auth/login.html')


def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if check_username_password(username, password):
        return redirect(url_for('dashboard.user_dashboard'))
    flash('Login failed. Try admin/password.')
    return redirect(url_for('auth.login'))


def show_register():
    return render_template('auth/register.html')


def show_forgot_password():
    return render_template('auth/forgot_password.html')


def show_reset_password():
    return render_template('auth/reset_password.html')


def show_verify_otp():
    return render_template('auth/verify_otp.html')


def show_change_password():
    return render_template('auth/change_password.html')
