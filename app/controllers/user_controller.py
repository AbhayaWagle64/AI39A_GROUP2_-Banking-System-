import os
<<<<<<< HEAD
from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

=======
from flask import flash, redirect, url_for, session, render_template, request
>>>>>>> abhaya-wagle
from app.database import Database


class UserController:
    def __init__(self, app=None):
        from app.controllers.auth_controller import AuthController
        if app:
            self.auth_controller = AuthController(app)
        else:
            self.auth_controller = None
<<<<<<< HEAD
        self.upload_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "app", "static", "uploads"
        )
=======
        self.upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "static", "uploads")
>>>>>>> abhaya-wagle
        os.makedirs(self.upload_folder, exist_ok=True)
        self.allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp"}

    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions

    def get_current_user(self):
<<<<<<< HEAD
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
=======
        if self.auth_controller:
            return self.auth_controller.get_current_user()
        return None
>>>>>>> abhaya-wagle

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
<<<<<<< HEAD
            uploaded_image=uploaded_image,
=======
            uploaded_image=uploaded_image
>>>>>>> abhaya-wagle
        )

    def profile_management(self):
        user = self.get_current_user()
        uploaded_image = session.get("uploaded_image")

        if request.method == "POST":
<<<<<<< HEAD
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
=======
            full_name = request.form.get("full_name", user["full_name"] if user else "")
            email = request.form.get("email", user["email"] if user else "")
            phone = request.form.get("phone", user["phone"] if user else "")
            address = request.form.get("address", user["address"] if user else "")

            file = request.files.get("profile_image")

>>>>>>> abhaya-wagle
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

<<<<<<< HEAD
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
=======
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
            db.close()

            if password:
                from werkzeug.security import generate_password_hash
                db = Database()
                db.execute(
                    "UPDATE register SET password=%s WHERE username=%s",
                    (generate_password_hash(password), session.get("user_id"))
                )
                db.execute(
                    "UPDATE login SET password=%s WHERE username=%s",
                    (generate_password_hash(password), session.get("user_id"))
                )
                db.close()

            user_id = session.get("user_id")
            login_data = None
            reg_data = None
            db = Database()
            login_data = db.fetch_one("SELECT * FROM login WHERE username = %s", (user_id,))
            reg_data = db.fetch_one("SELECT * FROM register WHERE username = %s", (user_id,))
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
>>>>>>> abhaya-wagle
            return redirect(url_for("user.profile"))

        return render_template(
            "profile_management.html",
            user=user,
<<<<<<< HEAD
            uploaded_image=uploaded_image,
=======
            uploaded_image=uploaded_image
>>>>>>> abhaya-wagle
        )

    def admin_users(self):
        user = self.get_current_user()
<<<<<<< HEAD
        try:
            db = Database()
            users = db.fetch_all("SELECT * FROM register ORDER BY username")
            db.close()
        except Exception:
            users = []
            flash("Unable to load users.", "danger")
=======
        db = Database()
        users = db.fetch_all("SELECT * FROM register ORDER BY username")
        db.close()
>>>>>>> abhaya-wagle
        return render_template("user_management.html", user=user, users=users)
