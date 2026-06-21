from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import Database


auth = Blueprint("auth", __name__)


def _password_matches(stored_password, submitted_password):
    return check_password_hash(stored_password, submitted_password) or stored_password == submitted_password


@auth.route("/")
def home():
    return redirect(url_for("auth.register"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        dob = request.form.get("dob", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password") or request.form.get("confirmPassword", "")
        pan = request.form.get("pan", "").strip()
        referral = request.form.get("referral", "").strip()

        if not fullname or not email or not phone or not password:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        username = phone or email.split("@")[0]
        hashed_password = generate_password_hash(password)

        try:
            db = Database()
            db.execute(
                """
                INSERT INTO register
                (username, password, full_name, email, phone, customer_id, epaisa_id, address, account_type, date_joined)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    username,
                    hashed_password,
                    fullname,
                    email,
                    phone,
                    f"CUST-{phone[-6:] if len(phone) >= 6 else username[-6:]}",
                    f"eP-{phone}" if phone.startswith("98") and len(phone) == 10 else f"eP-{username[-6:]}",
                    "",
                    "Savings",
                    dob or "2026-01-01",
                )
            )
            db.execute(
                "INSERT INTO login (username, password, full_name, epaisa_id) VALUES (%s, %s, %s, %s)",
                (username, hashed_password, fullname, f"eP-{phone}" if phone.startswith("98") and len(phone) == 10 else f"eP-{username[-6:]}"),
            )
            db.close()
        except Exception:
            flash("Registration could not be completed. Please try again later.", "danger")
            return render_template("register.html")

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("email") or request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not identifier or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")

        try:
            db = Database()
            user = db.fetch_one(
                """
                SELECT r.*, l.full_name
                FROM register r
                JOIN login l ON l.username = r.username
                WHERE r.email = %s OR r.username = %s
                """,
                (identifier, identifier),
            )
            db.close()
        except Exception:
            flash("Login service is unavailable. Please try again later.", "danger")
            return render_template("login.html")

        if not user or not _password_matches(user["password"], password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session["user_id"] = user["username"]
        session["user"] = {
            "username": user["username"],
            "full_name": user.get("full_name") or user.get("full_name"),
            "email": user["email"],
            "phone": user["phone"],
            "account_type": user.get("account_type", "Savings"),
        }

        flash("Login successful.", "success")
        return redirect(url_for("user.home"))

    return render_template("login.html")


@auth.route("/terms")
def terms():
    return render_template("terms.html")


@auth.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@auth.route("/reset-password")
def reset_password():
    return render_template("reset_password.html")


@auth.route("/verify-otp")
def verify_otp():
    return render_template("verify_otp.html")


@auth.route("/change-password")
def change_password():
    return render_template("change_password.html")
