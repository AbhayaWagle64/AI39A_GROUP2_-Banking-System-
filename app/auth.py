from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "message": "User not authenticated"}), 401
            flash('Please login to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "message": "User not authenticated"}), 401
            flash('Please login to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        user = session.get('user', {})
        if user.get('account_type') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated_function