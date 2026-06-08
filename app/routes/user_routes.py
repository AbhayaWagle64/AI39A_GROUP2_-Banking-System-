import os
import uuid
import re
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, url_for
from werkzeug.security import generate_password_hash
from app.auth import login_required
from app.database import Database

main = Blueprint("user", __name__)

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "static", "uploads"
)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_customer_id(username):
    customer_id = 10001
    try:
        db = Database()
        result = db.fetch_one("SELECT COUNT(*) AS total FROM register")
        db.close()
        if result:
            customer_id = 10001 + result['total']
    except Exception:
        pass
    return f"SB-{customer_id}"


def get_current_user():
    from app.routes.auth_routes import login_model, register_model
    user_id = session.get("user_id")
    if not user_id:
        return None
    login_data = login_model.find_by_username(user_id)
    if not login_data:
        return None
    reg_data = register_model.find_by_username(user_id)
    return {
        "username": user_id,
        "full_name": login_data.get("full_name", user_id),
        "customer_id": get_customer_id(user_id),
        "email": reg_data.get("email", "") if reg_data else "",
        "phone": reg_data.get("phone", "") if reg_data else "",
        "address": reg_data.get("address", "") if reg_data else "",
        "account_type": reg_data.get("account_type", "Savings") if reg_data else "Savings",
        "date_joined": reg_data.get("date_joined", "") if reg_data else "",
        "balance": "12,450.00"
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
            "balance": "12,450.00"
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
    return render_template("wallet.html", user=user)


@main.route("/transactions")
@login_required
def transactions():
    user = get_current_user()
    return render_template("transactions.html", user=user)


@main.route("/admin/users")
@login_required
def admin_users():
    user = get_current_user()
    db = Database()
    users = db.fetch_all("SELECT * FROM register ORDER BY email")
    db.close()
    return render_template("user_management.html", user=user, users=users)
