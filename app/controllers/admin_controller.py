# app/controllers/admin_controller.py
# Admin-only pages for system administration.

from flask import render_template


def show_admin_dashboard():
    return render_template('admin/admin_dashboard.html')


def show_manage_users():
    return render_template('admin/manage_users.html')


def show_manage_transaction():
    return render_template('admin/manage_transaction.html')


def show_fraud_reports():
    return render_template('admin/fraud_reports.html')


def show_system_logs():
    return render_template('admin/system_logs.html')


def show_admin_settings():
    return render_template('admin/admin_settings.html')


def show_user_details():
    return render_template('admin/user_details.html')
