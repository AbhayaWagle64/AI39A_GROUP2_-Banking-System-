from datetime import datetime
import csv
import io
import json
import zipfile

from flask import Blueprint, jsonify, render_template, redirect, url_for, session, flash, request, send_file

from app.auth import login_required
from app.database import Database
from app.models.admin_model import AdminModel
from app.models.wallet_model import WalletModel

main = Blueprint("admin", __name__)
admin_model = AdminModel()
wallet_model = WalletModel()

SUCCESSFUL_STATUSES = ("completed", "merchant_payment", "recharge", "bank", "nmb", "global ime", "standard chartered")
SUCCESSFUL_STATUS_SQL = ", ".join(f"'{status}'" for status in SUCCESSFUL_STATUSES)


def _ensure_admin():
    return session.get("is_admin")


def _failure_reason(status):
    status = (status or "").lower()
    if status == "recharge_failed":
        return "Recharge failed after OTP, timeout, or network issue"
    if status == "failed_otp":
        return "Wrong or expired OTP"
    if status == "failed_internet":
        return "Internet failure"
    if status == "failed_processed":
        return "Processed but not completed"
    if status == "failed":
        return "Unsuccessful transaction"
    return "Unsuccessful transaction"


def _fetch_transactions(include_wrong_only=False):
    db = Database()
    try:
        if include_wrong_only:
            rows = db.fetch_all(
                f"""
                SELECT id, transaction_date, sender_email, sender_epaisa_id,
                       receiver_email, receiver_epaisa_id, amount, status
                FROM transactions
                WHERE COALESCE(LOWER(status), '') NOT IN ({SUCCESSFUL_STATUS_SQL})
                ORDER BY transaction_date DESC
                """
            )
        else:
            rows = db.fetch_all(
                """
                SELECT id, transaction_date, sender_email, sender_epaisa_id,
                       receiver_email, receiver_epaisa_id, amount, status
                FROM transactions
                ORDER BY transaction_date DESC
                """
            )
    finally:
        db.close()

    for row in rows:
        if include_wrong_only:
            row["failure_reason"] = _failure_reason(row.get("status"))
    return rows


def _fetch_user_growth():
    db = Database()
    try:
        rows = db.fetch_all(
            """
            SELECT date_joined, COUNT(*) AS new_users
            FROM register
            GROUP BY date_joined
            ORDER BY date_joined
            """
        )
    finally:
        db.close()

    cumulative = 0
    result = []
    for row in rows:
        new_users = int(row.get("new_users") or 0)
        cumulative += new_users
        result.append({
            "date_joined": row.get("date_joined") or "",
            "new_users": new_users,
            "cumulative_users": cumulative
        })
    return result


def _transaction_csv_rows(include_wrong_only=False):
    rows = _fetch_transactions(include_wrong_only)
    csv_rows = []
    for row in rows:
        csv_rows.append([
            row.get("id") or "",
            row.get("transaction_date").strftime("%Y-%m-%d %H:%M:%S") if row.get("transaction_date") else "",
            row.get("sender_email") or "",
            row.get("sender_epaisa_id") or "",
            row.get("receiver_email") or "",
            row.get("receiver_epaisa_id") or "",
            row.get("amount") or 0,
            row.get("status") or "",
            row.get("failure_reason") or ""
        ])
    return csv_rows


def _user_growth_csv_rows():
    return [
        [row["date_joined"], row["new_users"], row["cumulative_users"]]
        for row in _fetch_user_growth()
    ]


def _write_csv(headers, rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue()


def _report_filename(extension):
    return f"epaisa_admin_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"


@main.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    db = Database()
    users = db.fetch_all("SELECT username, full_name, epaisa_id, balance, email, phone, date_joined FROM register ORDER BY date_joined DESC")
    db.close()
    return render_template("admin/dashboard.html", users=users)


@main.route("/admin/wallet")
@login_required
def admin_wallet():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    db = Database()
    total_users = db.fetch_one("SELECT COUNT(*) as total FROM register")
    db.close()
    return render_template("admin/wallet.html", total_users=total_users)


@main.route("/admin/transactions")
@login_required
def admin_transactions():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    transactions = _fetch_transactions()
    return render_template("admin/transactions.html", transactions=transactions)


@main.route("/admin/report")
@login_required
def admin_report():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    db = Database()
    try:
        total_users = db.fetch_one("SELECT COUNT(*) as total FROM register")
    finally:
        db.close()

    user_growth = _fetch_user_growth()
    return render_template(
        "admin/report.html",
        transactions=_fetch_transactions(),
        wrong_transactions=_fetch_transactions(include_wrong_only=True),
        total_users=total_users,
        user_growth=user_growth,
        user_growth_json=json.dumps(user_growth)
    )


@main.route("/admin/report/transactions.csv")
@login_required
def export_transactions_csv():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    csv_content = _write_csv(
        [
            "id", "transaction_date", "sender_email", "sender_epaisa_id",
            "receiver_email", "receiver_epaisa_id", "amount", "status", "failure_reason"
        ],
        _transaction_csv_rows()
    )
    return send_file(
        io.BytesIO(csv_content.encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=_report_filename("transactions.csv")
    )


@main.route("/admin/report/wrong-transactions.csv")
@login_required
def export_wrong_transactions_csv():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    csv_content = _write_csv(
        [
            "id", "transaction_date", "sender_email", "sender_epaisa_id",
            "receiver_email", "receiver_epaisa_id", "amount", "status", "failure_reason"
        ],
        _transaction_csv_rows(include_wrong_only=True)
    )
    return send_file(
        io.BytesIO(csv_content.encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=_report_filename("wrong_transactions.csv")
    )


@main.route("/admin/report/user-growth.csv")
@login_required
def export_user_growth_csv():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    csv_content = _write_csv(
        ["date_joined", "new_users", "cumulative_users"],
        _user_growth_csv_rows()
    )
    return send_file(
        io.BytesIO(csv_content.encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=_report_filename("user_growth.csv")
    )


@main.route("/admin/report/download-all")
@login_required
def download_admin_report_zip():
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as report_zip:
        report_zip.writestr(
            "all_transactions.csv",
            _write_csv(
                [
                    "id", "transaction_date", "sender_email", "sender_epaisa_id",
                    "receiver_email", "receiver_epaisa_id", "amount", "status", "failure_reason"
                ],
                _transaction_csv_rows()
            ).encode("utf-8-sig")
        )
        report_zip.writestr(
            "wrong_transactions.csv",
            _write_csv(
                [
                    "id", "transaction_date", "sender_email", "sender_epaisa_id",
                    "receiver_email", "receiver_epaisa_id", "amount", "status", "failure_reason"
                ],
                _transaction_csv_rows(include_wrong_only=True)
            ).encode("utf-8-sig")
        )
        report_zip.writestr(
            "user_growth.csv",
            _write_csv(
                ["date_joined", "new_users", "cumulative_users"],
                _user_growth_csv_rows()
            ).encode("utf-8-sig")
        )

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=_report_filename("zip")
    )


@main.route("/admin/edit-user/<username>", methods=["GET", "POST"])
@login_required
def edit_user(username):
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    db = Database()
    user = db.fetch_one("SELECT * FROM register WHERE username = %s", (username,))

    if request.method == "POST":
        full_name = request.form.get("full_name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        balance = request.form.get("balance", "0")

        db.execute(
            "UPDATE register SET full_name = %s, email = %s, phone = %s, address = %s, balance = %s WHERE username = %s",
            (full_name, email, phone, address, balance, username)
        )
        db.execute(
            "UPDATE login SET full_name = %s WHERE username = %s",
            (full_name, username)
        )
        db.close()
        flash("User updated successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))

    db.close()
    return render_template("admin/edit_user.html", user=user)


@main.route("/admin/delete-user/<username>", methods=["POST"])
@login_required
def delete_user(username):
    if not _ensure_admin():
        flash("Admin access required.", "danger")
        return redirect(url_for("user.dashboard"))

    db = Database()
    db.execute("DELETE FROM register WHERE username = %s", (username,))
    db.execute("DELETE FROM login WHERE username = %s", (username,))
    db.close()
    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.admin_dashboard"))


@main.route("/api/admin/user-stats")
@login_required
def user_stats():
    if not _ensure_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403

    db = Database()
    top_users = db.fetch_all(
        "SELECT full_name, balance FROM register ORDER BY balance DESC LIMIT 5"
    )
    db.close()

    return jsonify({
        "success": True,
        "top_users": top_users
    })
