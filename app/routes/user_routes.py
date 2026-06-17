import os
import uuid
import re
import json
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from werkzeug.security import generate_password_hash
from app.auth import login_required
from app.database import Database
from app.models.login_model import LoginModel
from app.models.register_model import RegisterModel
from app.models.wallet_model import WalletModel

main = Blueprint("user", __name__)
login_model = LoginModel()
register_model = RegisterModel()
wallet_model = WalletModel()

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "static", "uploads"
)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    login_data = login_model.find_by_username(user_id)
    if not login_data:
        return None
    reg_data = register_model.find_by_username(user_id)
    balance = 0.0
    if reg_data and reg_data.get("balance"):
        try:
            balance = float(reg_data["balance"])
        except (ValueError, TypeError):
            balance = 0.0
    epaisa_id = ""
    if reg_data and reg_data.get("epaisa_id"):
        epaisa_id = reg_data["epaisa_id"]
    else:
        epaisa_id = login_data.get("epaisa_id", "")
    tx_count = wallet_model.get_transaction_count(user_id)
    return {
        "username": user_id,
        "full_name": login_data.get("full_name", user_id),
        "customer_id": epaisa_id,
        "epaisa_id": epaisa_id,
        "email": reg_data.get("email", "") if reg_data else "",
        "phone": reg_data.get("phone", "") if reg_data else "",
        "address": reg_data.get("address", "") if reg_data else "",
        "account_type": reg_data.get("account_type", "Savings") if reg_data else "Savings",
        "date_joined": reg_data.get("date_joined", "") if reg_data else "",
        "balance": balance,
        "transaction_count": tx_count
    }


@main.route("/")
@login_required
def home():
    user = get_current_user()
    return render_template("dashboard.html", user=user)


@main.route("/dashboard")
@login_required
def dashboard():
    user = get_current_user()
    return render_template("dashboard.html", user=user)


@main.route("/profile")
@login_required
def profile():
    user = get_current_user()
    uploaded_image = session.get("uploaded_image")
    return render_template(
        "profile.html",
        user=user,
        uploaded_image=uploaded_image
    )


@main.route("/profile-management", methods=["GET", "POST"])
@login_required
def profile_management():
    user = get_current_user()
    uploaded_image = session.get("uploaded_image")

    if request.method == "POST":
        full_name = request.form.get("full_name", user["full_name"] if user else "")
        email = request.form.get("email", user["email"] if user else "")
        phone = request.form.get("phone", user["phone"] if user else "")
        address = request.form.get("address", user["address"] if user else "")

        file = request.files.get("profile_image")

        if file and file.filename and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)

            old_image = session.get("uploaded_image")
            if old_image:
                old_path = os.path.join(UPLOAD_FOLDER, old_image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            session["uploaded_image"] = filename

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password and password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template(
                "profile_management.html",
                user=user,
                uploaded_image=uploaded_image
            )

        db = Database()
        db.execute(
            "UPDATE register SET full_name=%s, email=%s, phone=%s, address=%s WHERE username=%s",
            (full_name, email, phone, address, session.get("user_id"))
        )
        db.execute(
            "UPDATE login SET full_name=%s WHERE username=%s",
            (full_name, session.get("user_id"))
        )
        if password:
            db.execute(
                "UPDATE login SET password=%s WHERE username=%s",
                (generate_password_hash(password), session.get("user_id"))
            )
            db.execute(
                "UPDATE register SET password=%s WHERE username=%s",
                (generate_password_hash(password), session.get("user_id"))
            )
        db.close()

        updated_user = {
            "username": session.get("user_id"),
            "full_name": full_name,
            "customer_id": user["customer_id"] if user else f"SB-{10001}",
            "email": email,
            "phone": phone,
            "address": address,
            "account_type": user["account_type"] if user else "Savings",
            "date_joined": user["date_joined"] if user else "",
            "balance": float(user["balance"]) if user and user.get("balance") else 0.0
        }

        flash("Profile updated successfully!", "success")
        return redirect(url_for("user.profile"))

    return render_template(
        "profile_management.html",
        user=user,
        uploaded_image=uploaded_image
    )


@main.route("/wallet")
@login_required
def wallet():
    user = get_current_user()
    return render_template("wallet/wallet.html", user=user)


@main.route("/api/send-money", methods=["POST"])
def send_money():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    raw_data = request.get_data(as_text=True)
    if not raw_data:
        return jsonify({"success": False, "message": "Invalid request - no data received"}), 400
    
    try:
        data = json.loads(raw_data)
    except Exception as e:
        return jsonify({"success": False, "message": f"JSON parse error: {str(e)}", "raw": raw_data[:200]}), 400
    
    if data is None or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid request - empty JSON", "data_type": type(data).__name__, "raw": raw_data[:200]}), 400
    
    if not data.get("epaisaNumber") or not data.get("amount"):
        return jsonify({"success": False, "message": "Missing required fields", "data": data}), 400

    recipient_epaisa = data.get("epaisaNumber", "") or ""
    recipient_epaisa = recipient_epaisa.strip() if recipient_epaisa else ""
    amount_val = data.get("amount")
    amount_str = str(amount_val).strip() if amount_val is not None else "0"
    recipient_name = data.get("accountHolder", "") or ""
    recipient_name = recipient_name.strip() if recipient_name else ""

    if not recipient_epaisa:
        return jsonify({"success": False, "message": "Recipient ePaisa ID is required"}), 400

    try:
        amount = float(amount_str) if amount_str else 0
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than 0"}), 400

    user = get_current_user()
    if not user:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    db = Database()
    recipient = db.fetch_one(
        "SELECT username, email, phone, epaisa_id, balance FROM register WHERE epaisa_id = %s OR phone = %s",
        (recipient_epaisa, recipient_epaisa)
    )
    if not recipient:
        db.close()
        return jsonify({"success": False, "message": "Recipient not found"}), 400

    if recipient["username"] == user["username"]:
        db.close()
        return jsonify({"success": False, "message": "Cannot send to yourself"}), 400

    recipient_balance = float(recipient.get("balance", 0)) if recipient.get("balance") else 0.0
    sender_balance = user.get("balance", 0.0)
    if isinstance(sender_balance, str):
        try:
            sender_balance = float(sender_balance)
        except (ValueError, TypeError):
            sender_balance = 0.0
    if sender_balance < amount:
        db.close()
        return jsonify({"success": False, "message": "Insufficient balance"}), 400

    sender_balance = sender_balance - amount
    recipient_balance = recipient_balance + amount
    db.execute("UPDATE register SET balance = %s WHERE username = %s", (sender_balance, user["username"]))
    db.execute("UPDATE register SET balance = %s WHERE username = %s", (recipient_balance, recipient["username"]))

    sender_email = user.get("email") or ""
    sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
    receiver_email = recipient.get("email") or ""
    receiver_epaisa_id = recipient.get("epaisa_id") or recipient.get("customer_id") or recipient.get("username") or ""

    db.execute(
        "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (%s, %s, %s, %s, %s, 'completed')",
        (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount)
    )
    db.close()

    return jsonify({
        "success": True,
        "message": "Transfer successful",
        "new_balance": sender_balance
    }), 200


@main.route("/transactions")
@login_required
def transactions():
    user = get_current_user()
    rows = wallet_model.get_all_transactions(user["username"] if user else "")
    return render_template("transactions.html", user=user, rows=rows)


@main.route("/admin/users")
@login_required
def admin_users():
    user = get_current_user()
    db = Database()
    users = db.fetch_all("SELECT * FROM register ORDER BY email")
    db.close()
    return render_template("user_management.html", user=user, users=users)