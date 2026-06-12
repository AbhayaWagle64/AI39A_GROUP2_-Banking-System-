import os
import re
import uuid
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.register_model import RegisterModel
from app.models.login_model import LoginModel
from app.models.wallet_model import WalletModel
from app.database import Database

main = Blueprint("auth", __name__)

register_model = RegisterModel()
login_model = LoginModel()
wallet_model = WalletModel()

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "static", "uploads"
)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_phone(phone):
    return bool(re.fullmatch(r'98\d{8}', phone))


def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


def get_customer_id(username=None):
    customer_id = "EP-10001"
    db = Database()
    if username:
        result = db.fetch_one("SELECT epaisa_id, customer_id, phone FROM register WHERE username = %s", (username,))
        if result:
            db.close()
            if result.get("epaisa_id"):
                return result["epaisa_id"]
            if result.get("customer_id"):
                return result["customer_id"]
            phone = result.get("phone", "")
            if phone and phone.startswith("98") and len(phone) >= 10:
                return f"SB-{phone}"
            return f"EP-10001"
    result = db.fetch_one("SELECT COUNT(*) AS total FROM register")
    db.close()
    if result:
        customer_id = f"EP-{10001 + result['total']}"
    return customer_id


def _generate_epaisa_id(phone=None, db=None):
    if phone and phone.startswith("98") and len(phone) >= 10:
        return f"eP-{phone}"
    base = 1001
    if db:
        result = db.fetch_one(
            "SELECT CAST(SUBSTRING_INDEX(epaisa_id, '-', -1) AS UNSIGNED) AS num FROM register WHERE epaisa_id REGEXP %s ORDER BY num DESC LIMIT 1",
            ("^eP-[0-9]+$",)
        )
        if result and result.get("num"):
            base = int(result["num"]) + 1
    return f"eP-{base}"


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    login_data = login_model.find_by_username(user_id)
    if not login_data:
        session.clear()
        return None
    reg_data = register_model.find_by_username(user_id)
    balance = 0.0
    try:
        if reg_data and reg_data.get("balance"):
            balance = float(reg_data["balance"])
    except (ValueError, TypeError):
        balance = 0.0
    epaisa_id = ""
    if reg_data and reg_data.get("epaisa_id"):
        epaisa_id = reg_data["epaisa_id"]
    else:
        epaisa_id = login_data.get("epaisa_id", "")
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
        "transaction_count": wallet_model.get_transaction_count(user_id)
    }


@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username/email and password are required.', 'danger')
            return render_template("login.html")

        login_data = login_model.find_by_username(username)
        if login_data:
            reg_data = register_model.find_by_username(username)
            if not reg_data:
                flash('Account not found.', 'danger')
                return render_template("login.html")
            if check_password_hash(login_data['password'], password):
                epaisa_id = login_data.get("epaisa_id") or ""
                if reg_data:
                    epaisa_id = reg_data.get("epaisa_id") or epaisa_id
                if epaisa_id:
                    login_model.create(username, login_data['password'], login_data['full_name'], epaisa_id=epaisa_id)
                session['user_id'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('user.wallet'))
            else:
                flash('Wrong username or password.', 'danger')
                return render_template("login.html")
        
        reg_data = register_model.find_by_username(username)
        if not reg_data:
            db = Database()
            results = db.fetch_all("SELECT * FROM register WHERE email = %s", (username,))
            db.close()
            if results:
                reg_data = results[0]
        
        if reg_data:
            if check_password_hash(reg_data['password'], password):
                epaisa_id = reg_data.get("epaisa_id") or f"eP-{reg_data['phone']}"
                login_model.create(reg_data['username'], reg_data['password'], reg_data['full_name'], epaisa_id=epaisa_id)
                session['user_id'] = reg_data['username']
                flash('Login successful!', 'success')
                return redirect(url_for('user.wallet'))
            else:
                flash('Wrong username or password.', 'danger')
                return render_template("login.html")
        else:
            flash('Wrong username or password.', 'danger')
            return render_template("login.html")

    return render_template("login.html")


@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template("register.html")

        if not full_name:
            flash('Full name is required.', 'danger')
            return render_template("register.html")

        if not validate_phone(phone):
            flash('Phone number must be exactly 10 digits starting with 98 (e.g. 9812345678).', 'danger')
            return render_template("register.html")

        if '@' not in email:
            flash('Please enter a valid email address.', 'danger')
            return render_template("register.html")

        if not validate_password(password):
            flash('Password must be at least 8 characters with 1 uppercase letter, 1 number, and 1 special character.', 'danger')
            return render_template("register.html")

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template("register.html")

        username = email

        if register_model.find_by_email(email):
            flash("An account with this email already exists.", 'danger')
            return render_template("register.html")

        if register_model.find_by_username(username):
            flash("An account with this username already exists.", 'danger')
            return render_template("register.html")

        if register_model.find_by_phone(phone):
            flash("An account with this phone number already exists.", 'danger')
            return render_template("register.html")

        password_hash = generate_password_hash(password)
        db = Database()
        epaisa_id = _generate_epaisa_id(phone=phone, db=db)
        customer_id = f"SB-{phone}" if phone.startswith("98") else f"SB-{10001}"
        db.execute(
            "INSERT INTO register (username, password, full_name, email, phone, customer_id, epaisa_id, balance, address, account_type, date_joined) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (username, password_hash, full_name, email, phone, customer_id, epaisa_id, 1000.0, '', 'Savings', '2026-01-01')
        )
        db.execute(
            "INSERT INTO login (username, password, full_name, epaisa_id) VALUES (%s, %s, %s, %s)",
            (username, password_hash, full_name, epaisa_id)
        )
        db.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html")


@main.route("/logout", methods=['GET', 'POST'])
def logout():
    user_id = session.get("user_id")
    if user_id:
        login_model.delete(user_id)
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))