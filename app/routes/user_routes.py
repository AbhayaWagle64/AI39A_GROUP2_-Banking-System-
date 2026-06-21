from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.controllers.user_controller import UserController

user_bp = Blueprint("user", __name__)
user_controller = UserController()


@user_bp.route("/")
def home():
    return render_template("home.html")


@user_bp.route("/profile")
def profile():
    return user_controller.profile()


@user_bp.route("/profile-management", methods=["GET", "POST"])
def profile_management():
    return user_controller.profile_management()


@user_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
