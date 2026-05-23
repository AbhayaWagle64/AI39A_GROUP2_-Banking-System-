from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("profile/management")
def profile_manage():
    return render_template("profile_management.html")
