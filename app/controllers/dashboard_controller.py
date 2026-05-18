# app/controllers/dashboard_controller.py
# Controllers for dashboard pages.

from flask import render_template


def show_user_dashboard():
    return render_template('dashboard/user_dashboard.html')


def show_dashboard():
    return render_template('dashboard/dashboard.html')


def show_admin_dashboard():
    return render_template('dashboard/admin_dashboard.html')


def show_analytics():
    return render_template('dashboard/analytics.html')
