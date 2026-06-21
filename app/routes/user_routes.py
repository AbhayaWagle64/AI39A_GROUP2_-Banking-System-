import os
import uuid
import re
import json
import logging
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify, current_app
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
logger = logging.getLogger(__name__)
 
def _get_mailer():
    from flask import current_app
    return getattr(current_app, "mailer", None)
 
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "static", "uploads"
)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
 
 
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def insert_failed_transaction(user, amount, receiver_epaisa_id="", receiver_email="", status="failed"):
    if not user:
        return

    sender_email = user.get("email") or ""
    sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
    db = Database()
    db.execute(
        "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
        (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status)
    )
    db.close()
 
 
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
 
 
@main.route("/api/lookup-user", methods=["POST"])
def lookup_user():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401
    
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return jsonify({"success": False, "message": "Invalid request"}), 400
    
    epaisa_id = data.get("epaisa_id", "").strip()
    
    if not epaisa_id:
        return jsonify({"success": False, "message": "ePaisa ID required"}), 400
    
    db = Database()
    user = db.fetch_one(
        "SELECT username, epaisa_id FROM register WHERE epaisa_id = ? OR phone = ? OR username = ?",
        (epaisa_id, epaisa_id, epaisa_id)
    )
    db.close()
    
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 400
    
    return jsonify({
        "success": True,
        "epaisa_id": user.get("epaisa_id", ""),
        "username": user.get("username", "")
    }), 200
 
 
@main.route("/")
@login_required
def home():
    user = get_current_user()
    return render_template("dashboard.html", user=user)
 
# DASHBOARD
@main.route("/dashboard")
@login_required
def dashboard():
    user = get_current_user()
    return render_template("dashboard.html", user=user)
 
#  PROFILE
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
            "UPDATE register SET full_name=?, email=?, phone=?, address=? WHERE username=?",
            (full_name, email, phone, address, session.get("user_id"))
        )
        db.execute(
            "UPDATE login SET full_name=? WHERE username=?",
            (full_name, session.get("user_id"))
        )
        if password:
            db.execute(
                "UPDATE login SET password=? WHERE username=?",
                (generate_password_hash(password), session.get("user_id"))
            )
            db.execute(
                "UPDATE register SET password=? WHERE username=?",
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
        "SELECT username, email, phone, epaisa_id, balance FROM register WHERE epaisa_id = ? OR phone = ?",
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
 
    session["pending_transaction"] = {
        "sender_username": user["username"],
        "sender_balance": sender_balance,
        "recipient_epaisa": recipient_epaisa,
        "recipient_name": recipient_name,
        "amount": amount,
    }
    db.close()
 
    return jsonify({
        "success": True,
        "message": "OK",
        "next": "otp",
        "redirect": url_for("user.verify_otp_page")
    }), 200
 
 
@main.route("/qr-code")
@login_required
def qr_code():
    user = get_current_user()
    epaisa_id = user.get("epaisa_id", user.get("username", ""))
 
    import qrcode
    import io
    from flask import send_file
 
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(epaisa_id)
    qr.make(fit=True)
 
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
 
    return send_file(buf, mimetype="image/png")
 
 
@main.route("/transactions")
@login_required
def transactions():
    user = get_current_user()
    rows = wallet_model.get_all_transactions(user["username"] if user else "")
    return render_template("transactions.html", user=user, rows=rows)


@main.route("/verify-otp")
@main.route("/verify-otp/<error>")
@login_required
def verify_otp_page(error=None):
    sender = get_current_user()
    pending = session.get("pending_transaction")
    if not pending or not sender or sender["username"] != pending.get("sender_username"):
        return redirect(url_for("user.wallet"))
    raw_email = sender.get("email", "") or ""
    local = raw_email.split("@")[0] if "@" in raw_email else raw_email
    domain = raw_email.split("@")[1] if "@" in raw_email else ""
    if len(local) > 2:
        masked = f"{local[:2]}{'*' * (len(local) - 2)}@{domain}"
    else:
        masked = f"{local[0]}{'*' * (len(local) - 1)}@{domain}"
    return render_template("wallet/verify_otp.html", user=sender, masked_email=masked, error=error)
 
 
@main.route("/transaction-success")
@login_required
def transaction_success():
    sender = get_current_user()
    pending = session.pop("pending_transaction", None)
    return render_template("wallet/success.html", user=sender, pending=pending)
 
 
@main.route("/transaction-failed")
@login_required
def transaction_failed():
    sender = get_current_user()
    pending = session.pop("pending_transaction", None)
    return render_template("wallet/failed.html", user=sender, pending=pending)
 
 
@main.route("/api/request-otp", methods=["POST"])
def request_otp():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401
 
    pending = session.get("pending_transaction")
    if not pending:
        return jsonify({"success": False, "message": "No pending transaction"}), 400
 
    sender = get_current_user()
    sender_email = sender.get("email", "").strip() if sender else ""
    if not sender_email:
        return jsonify({"success": False, "message": "No email found for user"}), 400
 
    mailer = _get_mailer()
    if not mailer or not mailer.is_configured:
        return jsonify({"success": False, "message": "Email service is not configured"}), 500
 
    otp = f"{secrets.randbelow(1000000):06d}"
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    session["verified_otp"] = otp
    session["otp_expires_at"] = expires_at.isoformat()
    session["otp_attempts"] = 0
 
    try:
        sent = mailer.send_otp(sender_email, otp, async_send=False)
        if not sent:
            raise RuntimeError("Mailer returned false")
        logger.info("OTP email sent to ?", sender_email)
    except Exception as exc:
        logger.exception("OTP email failed: ?", exc)
        _clear_otp_session()
        return jsonify({"success": False, "message": "Could not send OTP email. Please try again."}), 500
 
    return jsonify({
        "success": True,
        "message": "OTP sent to your email",
        "redirect": url_for("user.verify_otp_page"),
    }), 200
 
 
@main.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        code = (payload.get("otp") or "").strip()
    else:
        code = (request.form.get("otp") or "").strip()
    if not code or len(code) != 6 or not code.isdigit():
        pending = session.get("pending_transaction")
        if pending:
            user = get_current_user()
            if user:
                insert_failed_transaction(
                    user,
                    float(pending.get("amount", 0)),
                    pending.get("recipient_epaisa", ""),
                    "",
                    "failed_otp"
                )
        _clear_otp_session()
        session.pop("pending_transaction", None)
        return redirect(url_for("user.transaction_failed"))
    stored_otp = session.get("verified_otp")
    expires_at = session.get("otp_expires_at")
    attempts = int(session.get("otp_attempts", 0) or 0) + 1
    session["otp_attempts"] = attempts
    if attempts >= 5:
        pending = session.get("pending_transaction")
        if pending:
            user = get_current_user()
            if user:
                insert_failed_transaction(
                    user,
                    float(pending.get("amount", 0)),
                    pending.get("recipient_epaisa", ""),
                    "",
                    "failed_otp"
                )
        _clear_otp_session()
        session.pop("pending_transaction", None)
        return redirect(url_for("user.transaction_failed"))
    if not stored_otp or stored_otp != code:
        pending = session.get("pending_transaction")
        if pending:
            user = get_current_user()
            if user:
                insert_failed_transaction(
                    user,
                    float(pending.get("amount", 0)),
                    pending.get("recipient_epaisa", ""),
                    "",
                    "failed_otp"
                )
        return redirect(url_for("user.verify_otp_page", error="invalid"))
    if expires_at and datetime.fromisoformat(expires_at) < datetime.utcnow():
        pending = session.get("pending_transaction")
        if pending:
            user = get_current_user()
            if user:
                insert_failed_transaction(
                    user,
                    float(pending.get("amount", 0)),
                    pending.get("recipient_epaisa", ""),
                    "",
                    "failed_otp"
                )
        _clear_otp_session()
        session.pop("pending_transaction", None)
        return redirect(url_for("user.transaction_failed"))
 
    pending = session.get("pending_transaction")
    if not pending:
        return redirect(url_for("user.transaction_failed"))
 
    sender_username = pending.get("sender_username") or session.get("user_id")
    recipient_epaisa = pending.get("recipient_epaisa", "")
    recipient_name = pending.get("recipient_name", "")
    amount = float(pending.get("amount", 0))
 
    user = get_current_user()
    if not user or user["username"] != sender_username:
        return redirect(url_for("user.transaction_failed"))
 
    db = Database()
    recipient = db.fetch_one(
        "SELECT username, email, phone, epaisa_id, balance FROM register WHERE epaisa_id = ? OR phone = ?",
        (recipient_epaisa, recipient_epaisa)
    )
    if not recipient:
        user = get_current_user()
        if user:
            insert_failed_transaction(
                user,
                amount,
                recipient_epaisa,
                "",
                "failed"
            )
        _clear_otp_session()
        session.pop("pending_transaction", None)
        return redirect(url_for("user.transaction_failed"))
 
    if recipient["username"] == user["username"]:
        insert_failed_transaction(
            user,
            amount,
            recipient_epaisa,
            recipient.get("email") or "",
            "failed"
        )
        _clear_otp_session()
        session.pop("pending_transaction", None)
        return redirect(url_for("user.transaction_failed"))
 
    recipient_balance = float(recipient.get("balance", 0) or 0)
    sender_balance = float(user.get("balance", 0) or 0)
    if sender_balance < amount:
        insert_failed_transaction(
            user,
            amount,
            recipient_epaisa,
            recipient.get("email") or "",
            "failed"
        )
        _clear_otp_session()
        session.pop("pending_transaction", None)
        return redirect(url_for("user.transaction_failed"))
 
    sender_balance = sender_balance - amount
    recipient_balance = recipient_balance + amount
    db.execute("UPDATE register SET balance = ? WHERE username = ?", (sender_balance, user["username"]))
    db.execute("UPDATE register SET balance = ? WHERE username = ?", (recipient_balance, recipient["username"]))
 
    sender_email = user.get("email") or ""
    sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
    receiver_email = recipient.get("email") or ""
    receiver_epaisa_id = recipient.get("epaisa_id") or recipient.get("customer_id") or recipient.get("username") or ""
    db.execute(
        "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, 'completed')",
        (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount)
    )
    db.close()
    _clear_otp_session()
    session.pop("pending_transaction", None)

    return redirect(url_for("user.transaction_success"))

# RECHARGE
@main.route("/recharge")
@login_required
def recharge_page():
    user = get_current_user()
    return render_template("wallet/recharge.html", user=user)

# MERCHANT-PAY
@main.route("/merchant-pay")
@login_required
def merchant_pay_page():
    merchant_name = request.args.get("merchant", "Merchant")
    user = get_current_user()
    return render_template("wallet/merchant_pay.html", user=user, merchant_name=merchant_name)


@main.route("/api/merchant-pay", methods=["POST"])
@login_required
def merchant_pay():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    data = request.get_json(silent=True) or {}
    merchant = data.get("merchant", "").strip()
    amount = data.get("amount")

    if not merchant:
        return jsonify({"success": False, "message": "Merchant is required"}), 400

    try:
        amount_val = float(amount)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    if amount_val < 10:
        return jsonify({"success": False, "message": "Minimum amount is 10"}), 400

    user = get_current_user()
    if not user:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    sender_balance = float(user.get("balance", 0) or 0)
    if sender_balance < amount_val:
        return jsonify({"success": False, "message": "Insufficient balance"}), 400

    sender_balance = sender_balance - amount_val
    db = Database()
    db.execute(
        "UPDATE register SET balance = ? WHERE username = ?",
        (sender_balance, user["username"])
    )
    sender_email = user.get("email") or ""
    sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
    db.execute(
        "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, 'merchant_payment')",
        (sender_email, sender_epaisa_id, '', merchant, amount_val)
    )
    db.close()

    session["merchant_payment_success"] = {
        "merchant": merchant,
        "amount": amount_val
    }

    return jsonify({
        "success": True,
        "redirect": url_for("user.merchant_pay_success")
    }), 200


@main.route("/merchant-pay-success")
@login_required
def merchant_pay_success():
    user = get_current_user()
    payment = session.pop("merchant_payment_success", None)
    return render_template("wallet/merchant_pay_success.html", user=user, payment=payment)


@main.route("/recharge-success")
@login_required
def recharge_success():
    user = get_current_user()
    pending = session.pop("pending_recharge", None)
    return render_template("wallet/recharge_success.html", user=user, pending=pending)


@main.route("/recharge-failed")
@login_required
def recharge_failed():
    user = get_current_user()
    pending = session.pop("pending_recharge", None)
    return render_template("wallet/recharge_failed.html", user=user, pending=pending)


@main.route("/api/initiate-recharge", methods=["POST"])
def initiate_recharge():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    raw_data = request.get_data(as_text=True)
    if not raw_data:
        return jsonify({"success": False, "message": "Invalid request - no data received"}), 400

    try:
        data = json.loads(raw_data)
    except Exception:
        return jsonify({"success": False, "message": "Invalid JSON data"}), 400

    phone = data.get("phone", "").strip()
    operator = data.get("operator", "").strip()
    amount = data.get("amount")

    if not phone or not re.match(r"^[0-9]{10}$", phone):
        return jsonify({"success": False, "message": "Invalid phone number"}), 400

    if not operator:
        return jsonify({"success": False, "message": "Operator is required"}), 400

    try:
        amount_val = float(amount)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    if amount_val < 10:
        return jsonify({"success": False, "message": "Minimum amount is 10"}), 400

    user = get_current_user()
    if not user:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    sender_balance = user.get("balance", 0.0)
    if isinstance(sender_balance, str):
        try:
            sender_balance = float(sender_balance)
        except (ValueError, TypeError):
            sender_balance = 0.0

    if sender_balance < amount_val:
        return jsonify({"success": False, "message": "Insufficient balance"}), 400

    session["pending_recharge"] = {
        "sender_username": user["username"],
        "sender_balance": sender_balance,
        "phone": phone,
        "operator": operator,
        "amount": amount_val
    }

    return jsonify({
        "success": True,
        "message": "OK",
        "next": "otp",
        "redirect": url_for("user.verify_recharge_otp_page")
    }), 200


@main.route("/verify-recharge-otp")
@login_required
def verify_recharge_otp_page():
    sender = get_current_user()
    pending = session.get("pending_recharge")
    if not pending or not sender or sender["username"] != pending.get("sender_username"):
        return redirect(url_for("user.recharge_page"))
    raw_email = sender.get("email", "") or ""
    local = raw_email.split("@")[0] if "@" in raw_email else raw_email
    domain = raw_email.split("@")[1] if "@" in raw_email else ""
    if len(local) > 2:
        masked = f"{local[:2]}{'*' * (len(local) - 2)}@{domain}"
    else:
        masked = f"{local[0]}{'*' * (len(local) - 1)}@{domain}"
    return render_template("wallet/verify_otp.html", user=sender, masked_email=masked, error=None, recharge_mode=True)


@main.route("/api/request-recharge-otp", methods=["POST"])
def request_recharge_otp():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401

    pending = session.get("pending_recharge")
    if not pending:
        return jsonify({"success": False, "message": "No pending recharge"}), 400

    sender = get_current_user()
    sender_email = sender.get("email", "").strip() if sender else ""
    if not sender_email:
        return jsonify({"success": False, "message": "No email found for user"}), 400

    mailer = _get_mailer()
    if not mailer or not mailer.is_configured:
        return jsonify({"success": False, "message": "Email service is not configured"}), 500

    otp = f"{secrets.randbelow(1000000):06d}"
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    session["verified_otp"] = otp
    session["otp_expires_at"] = expires_at.isoformat()
    session["otp_attempts"] = 0

    try:
        sent = mailer.send_otp(sender_email, otp, async_send=False)
        if not sent:
            raise RuntimeError("Mailer returned false")
        logger.info("OTP email sent to ?", sender_email)
    except Exception as exc:
        logger.exception("OTP email failed: ?", exc)
        _clear_otp_session()
        return jsonify({"success": False, "message": "Could not send OTP email. Please try again."}), 500

    return jsonify({
        "success": True,
        "message": "OTP sent to your email",
        "redirect": url_for("user.verify_recharge_otp_page"),
    }), 200


@main.route("/api/verify-recharge-otp", methods=["POST"])
def verify_recharge_otp():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "User not authenticated"}), 401
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        code = (payload.get("otp") or "").strip()
    else:
        code = (request.form.get("otp") or "").strip()
    if not code or len(code) != 6 or not code.isdigit():
        pending = session.get("pending_recharge")
        if pending:
            user = get_current_user()
            if user:
                amount = float(pending.get("amount", 0))
                phone = pending.get("phone", "")
                operator = pending.get("operator", "")
                sender_email = user.get("email") or ""
                sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
                db = Database()
                db.execute(
                    "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (sender_email, sender_epaisa_id, '', f'{operator} - {phone}', amount, 'recharge_failed')
                )
                db.close()
        _clear_otp_session()
        session.pop("pending_recharge", None)
        return redirect(url_for("user.recharge_failed"))
    stored_otp = session.get("verified_otp")
    expires_at = session.get("otp_expires_at")
    attempts = int(session.get("otp_attempts", 0) or 0) + 1
    session["otp_attempts"] = attempts
    if attempts >= 5:
        pending = session.get("pending_recharge")
        if pending:
            user = get_current_user()
            if user:
                amount = float(pending.get("amount", 0))
                phone = pending.get("phone", "")
                operator = pending.get("operator", "")
                sender_email = user.get("email") or ""
                sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
                db = Database()
                db.execute(
                    "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (sender_email, sender_epaisa_id, '', f'{operator} - {phone}', amount, 'recharge_failed')
                )
                db.close()
        _clear_otp_session()
        session.pop("pending_recharge", None)
        return redirect(url_for("user.recharge_failed"))
    if not stored_otp or stored_otp != code:
        pending = session.get("pending_recharge")
        if pending:
            user = get_current_user()
            if user:
                insert_failed_transaction(
                    user,
                    float(pending.get("amount", 0)),
                    '',
                    f"{pending.get('operator', '')} - {pending.get('phone', '')}",
                    "failed_otp"
                )
        return redirect(url_for("user.verify_recharge_otp_page", error="invalid"))
    if expires_at and datetime.fromisoformat(expires_at) < datetime.utcnow():
        pending = session.get("pending_recharge")
        if pending:
            user = get_current_user()
            if user:
                amount = float(pending.get("amount", 0))
                phone = pending.get("phone", "")
                operator = pending.get("operator", "")
                sender_email = user.get("email") or ""
                sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
                db = Database()
                db.execute(
                    "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (sender_email, sender_epaisa_id, '', f'{operator} - {phone}', amount, 'recharge_failed')
                )
                db.close()
        _clear_otp_session()
        session.pop("pending_recharge", None)
        return redirect(url_for("user.recharge_failed"))

    pending = session.get("pending_recharge")
    if not pending:
        return redirect(url_for("user.recharge_failed"))

    sender_username = pending.get("sender_username") or session.get("user_id")
    phone = pending.get("phone", "")
    operator = pending.get("operator", "")
    amount = float(pending.get("amount", 0))

    user = get_current_user()
    if not user or user["username"] != sender_username:
        return redirect(url_for("user.recharge_failed"))

    db = Database()
    sender_balance = float(user.get("balance", 0) or 0)
    if sender_balance < amount:
        _clear_otp_session()
        session.pop("pending_recharge", None)
        db.close()
        return redirect(url_for("user.recharge_failed"))

    sender_balance = sender_balance - amount
    db.execute("UPDATE register SET balance = ? WHERE username = ?", (sender_balance, user["username"]))

    sender_email = user.get("email") or ""
    sender_epaisa_id = user.get("epaisa_id") or user.get("username") or ""
    db.execute(
        "INSERT INTO transactions (sender_email, sender_epaisa_id, receiver_email, receiver_epaisa_id, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
        (sender_email, sender_epaisa_id, '', f'{operator} - {phone}', amount, 'recharge')
    )
    db.close()
    _clear_otp_session()
    session.pop("pending_recharge", None)

    return redirect(url_for("user.recharge_success"))


def _clear_otp_session():
    session.pop("verified_otp", None)
    session.pop("otp_expires_at", None)


def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked_local = local[0] + "*" * (len(local) - 1)
    else:
        masked_local = local[:2] + "*" * (len(local) - 2)
    return f"{masked_local}@{domain}"
