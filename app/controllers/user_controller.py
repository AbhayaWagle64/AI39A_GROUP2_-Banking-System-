import os
from flask import flash, redirect, url_for, session, render_template, request
from app.database import Database


class UserController:
    def __init__(self, app=None):
        from app.controllers.auth_controller import AuthController
        if app:
            self.auth_controller = AuthController(app)
        else:
            self.auth_controller = None
        self.upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "static", "uploads")
        os.makedirs(self.upload_folder, exist_ok=True)
        self.allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp"}

    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions

    def get_current_user(self):
        if self.auth_controller:
            return self.auth_controller.get_current_user()
        return None

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
            uploaded_image=uploaded_image
        )

    def profile_management(self):
        user = self.get_current_user()
        uploaded_image = session.get("uploaded_image")

        if request.method == "POST":
            full_name = request.form.get("full_name", user["full_name"] if user else "")
            email = request.form.get("email", user["email"] if user else "")
            phone = request.form.get("phone", user["phone"] if user else "")
            address = request.form.get("address", user["address"] if user else "")

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
            db.close()

            if password:
                from werkzeug.security import generate_password_hash
                db = Database()
                db.execute(
                    "UPDATE register SET password=? WHERE username=?",
                    (generate_password_hash(password), session.get("user_id"))
                )
                db.execute(
                    "UPDATE login SET password=? WHERE username=?",
                    (generate_password_hash(password), session.get("user_id"))
                )
                db.close()

            user_id = session.get("user_id")
            login_data = None
            reg_data = None
            db = Database()
            login_data = db.fetch_one("SELECT * FROM login WHERE username = ?", (user_id,))
            reg_data = db.fetch_one("SELECT * FROM register WHERE username = ?", (user_id,))
            db.close()

            updated_user = {
                "username": user_id,
                "full_name": full_name,
                "customer_id": user["customer_id"] if user else f"SB-{10001}",
                "email": email,
                "phone": phone,
                "address": address,
                "account_type": reg_data.get("account_type", "Savings") if reg_data else "Savings",
                "date_joined": reg_data.get("date_joined", "") if reg_data else "",
                "balance": "12,450.00"
            }

            flash("Profile updated successfully!", "success")
            return redirect(url_for("user.profile"))

        return render_template(
            "profile_management.html",
            user=user,
            uploaded_image=uploaded_image
        )

    def admin_users(self):
        user = self.get_current_user()
        db = Database()
        users = db.fetch_all("SELECT * FROM register ORDER BY username")
        db.close()
        return render_template("user_management.html", user=user, users=users)
