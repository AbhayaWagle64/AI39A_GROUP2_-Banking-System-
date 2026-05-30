from flask import Blueprint, render_template, flash, redirect, url_for

class DashboardRoutes:
    def register(self):
        dashboard_bp = Blueprint('dashboard', __name__)

        @dashboard_bp.route('/dashboard')
        def dashboard():
            balance = 1000.00
            return render_template('dashboard.html', balance=balance)

        @dashboard_bp.route('/logout')
        def logout():
            flash('You have been logged out successfully.', 'success')
            return redirect(url_for('dashboard.dashboard'))

        return dashboard_bp