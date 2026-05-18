# app/controllers/home_controller.py
# Controller for the homepage and app root.

from flask import redirect, url_for, render_template


def show_home():
    return redirect(url_for('auth.login'))


def show_about():
    return render_template('dashboard/dashboard.html')
