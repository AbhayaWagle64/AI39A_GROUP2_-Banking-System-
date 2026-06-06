import os
import uuid
from flask import (
    Blueprint, render_template, url_for,
    redirect, request, session, flash
)

main = Blueprint("main", __name__)

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "app", "static", "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/")
def home():
    return render_template("login.html")


@main.route("/profile")
def profile():

    user = {
        "full_name": "Abhaya Wagle",
        "customer_id": "SB-10021",
        "email": "abhaya@gmail.com",
        "phone": "+977-98XXXXXXX",
        "address": "Kathmandu, Nepal",
        "account_type": "Savings",
        "date_joined": "2026-01-01"
    }

    uploaded_image = session.get("uploaded_image")

    return render_template(
        "profile.html",
        user=user,
        uploaded_image=uploaded_image
    )


@main.route("/profile-management", methods=["GET", "POST"])
def profile_management():

    user = {
        "full_name": "Abhaya Wagle",
        "email": "abhaya@gmail.com",
        "phone": "+977-98XXXXXXX",
        "address": "Kathmandu, Nepal"
    }

    uploaded_image = session.get("uploaded_image")

    if request.method == "POST":

        updated_user = {
            "full_name": request.form.get("full_name", user["full_name"]),
            "email": request.form.get("email", user["email"]),
            "phone": request.form.get("phone", user["phone"]),
            "address": request.form.get("address", user["address"])
        }

        file = request.files.get("profile_image")

        if file and file.filename and allowed_file(file.filename):

            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)

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
                user=updated_user,
                uploaded_image=uploaded_image
            )

        print("UPDATED USER:", updated_user)

        return redirect(url_for("main.profile"))

    return render_template(
        "profile_management.html",
        user=user,
        uploaded_image=uploaded_image
    )
