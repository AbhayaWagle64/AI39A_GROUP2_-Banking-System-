from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps
from app.auth import login_required
from app.database import Database

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access only.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/admin/dashboard")
@login_required
@admin_required
def dashboard():
    db = Database()

    total_users = db.fetch_one(
        "SELECT COUNT(*) as count FROM register"
    )["count"]

    new_users_today = db.fetch_one(
        "SELECT COUNT(*) as count FROM register WHERE date_joined = DATE_FORMAT(CURDATE(), '%Y-%m-%d')"
    )["count"]

    total_transactions = db.fetch_one(
        "SELECT COUNT(*) as count FROM transactions"
    )["count"]

    total_volume = db.fetch_one(
        "SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE status = 'completed'"
    )["total"]

    recent_activity = db.fetch_all("""
        SELECT id, sender_email, receiver_email,
               amount, status, transaction_date
        FROM transactions
        ORDER BY transaction_date DESC
        LIMIT 10
    """)

    failed_count = db.fetch_one("""
        SELECT COUNT(*) as count FROM transactions
        WHERE status = 'failed'
        AND transaction_date >= NOW() - INTERVAL 1 DAY
    """)["count"]

    db.close()

    return render_template("admin/dashboard.html",
                           total_users=total_users,
                           new_users_today=new_users_today,
                           total_transactions=total_transactions,
                           total_volume=total_volume,
                           recent_activity=recent_activity,
                           failed_count=failed_count
                           )
