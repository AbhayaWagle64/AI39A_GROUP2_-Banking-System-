import os

from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from app.database import Database


class UserController:
    def __init__(self):
        self.upload_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "static",
            "uploads",
        )
        os.makedirs(self.upload_folder, exist_ok=True)
        self.allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp"}

    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions

    def get_current_user(self):
        user_id = session.get("user_id")
        if not user_id:
            return None

        try:
            db = Database()
            user = db.fetch_one(
                """
                SELECT
                    r.username,
                    r.full_name,
                    r.email,
                    r.phone,
                    r.address,
                    r.customer_id,
                    r.epaisa_id,
                    r.balance,
                    r.account_type,
                    r.date_joined,
                    l.full_name AS login_full_name
                FROM register r
                LEFT JOIN login l ON l.username = r.username
                WHERE r.username = %s
                """,
                (user_id,),
            )
            db.close()
        except Exception:
            return session.get("user")

        if not user:
            return session.get("user")

        return {
            "username": user["username"],
            "full_name": user.get("full_name") or user.get("login_full_name") or user_id,
            "email": user.get("email", ""),
            "phone": user.get("phone", ""),
            "address": user.get("address", ""),
            "customer_id": user.get("customer_id", ""),
            "epaisa_id": user.get("epaisa_id", ""),
            "balance": user.get("balance", 0),
            "account_type": user.get("account_type", "Savings"),
            "date_joined": user.get("date_joined", ""),
        }

    def wallet(self):
        user = self.get_current_user()
        return render_template("wallet/wallet.html", user=user)

    def transactions(self):
        user = self.get_current_user()
        return render_template("transactions.html", user=user)

    def profile(self):
        user = self.get_current_user()
        uploaded_image = session.get("uploaded_image")
        return render_template(
            "profile.html",
            user=user,
            uploaded_image=uploaded_image,
        )

    def profile_management(self):
        user = self.get_current_user()
        uploaded_image = session.get("uploaded_image")

        if request.method == "POST":
            full_name = request.form.get("full_name", user.get("full_name", "") if user else "").strip()
            email = request.form.get("email", user.get("email", "") if user else "").strip()
            phone = request.form.get("phone", user.get("phone", "") if user else "").strip()
            address = request.form.get("address", user.get("address", "") if user else "").strip()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not full_name or not email or not phone:
                flash("Full name, email, and phone are required.", "danger")
                return render_template(
                    "profile_management.html",
                    user=user,
                    uploaded_image=uploaded_image,
                )

            if password and password != confirm_password:
                flash("Passwords do not match.", "danger")
                return render_template(
                    "profile_management.html",
                    user=user,
                    uploaded_image=uploaded_image,
                )

            file = request.files.get("profile_image")
            if file and file.filename and self.allowed_file(file.filename):
                ext = file.filename.rsplit(".", 1)[1].lower()
                filename = f"{os.urandom(8).hex()}.{ext}"
                filepath = os.path.join(self.upload_folder, filename)
                file.save(filepath)

                old_image = session.get("uploaded_image")
                if old_image:
                    old_path = os.path.join(self.upload_folder, old_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                session["uploaded_image"] = filename

            try:
                db = Database()
                db.execute(
                    """
                    UPDATE register
                    SET full_name=%s, email=%s, phone=%s, address=%s
                    WHERE username=%s
                    """,
                    (full_name, email, phone, address, session.get("user_id")),
                )
                db.execute(
                    "UPDATE login SET full_name=%s WHERE username=%s",
                    (full_name, session.get("user_id")),
                )

                if password:
                    hashed_password = generate_password_hash(password)
                    db.execute(
                        "UPDATE register SET password=%s WHERE username=%s",
                        (hashed_password, session.get("user_id")),
                    )
                    db.execute(
                        "UPDATE login SET password=%s WHERE username=%s",
                        (hashed_password, session.get("user_id")),
                    )

                db.close()
            except Exception:
                flash("Profile could not be updated. Please try again later.", "danger")
                return render_template(
                    "profile_management.html",
                    user=user,
                    uploaded_image=uploaded_image,
                )

            flash("Profile updated successfully.", "success")
            return redirect(url_for("user.profile"))

        return render_template(
            "profile_management.html",
            user=user,
            uploaded_image=uploaded_image,
        )

    def admin_users(self):
        user = self.get_current_user()
        try:
            db = Database()
            users = db.fetch_all("SELECT * FROM register ORDER BY username")
            db.close()
        except Exception:
            users = []
            flash("Unable to load users.", "danger")
        return render_template("user_management.html", user=user, users=users)
