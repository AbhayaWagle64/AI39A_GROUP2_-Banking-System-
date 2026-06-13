# app/controllers/auth_controller.py
"""
=============================================================
  OOP Concept: INHERITANCE & POLYMORPHISM
=============================================================
  - AuthController inherits BaseController.
  - Reuses helper methods from parent class.
=============================================================
"""

from flask import (
    Blueprint,
    render_template,
    request
)

from controllers.base_controller import BaseController


# ======================================
# Blueprint Creation
# ======================================

auth = Blueprint("auth", __name__)


# ======================================
# Auth Controller Class
# ======================================

class AuthController(BaseController):


    # ======================================
    # Register Method
    # ======================================

    def register(self):

        if request.method == "POST":

            (
                fullname,
                email,
                phone,
                dob,
                password,
                confirm_password,
                pan,
                referral

            ) = self.get_form_data(

                "fullname",
                "email",
                "phone",
                "dob",
                "password",
                "confirm_password",
                "pan",
                "referral"
            )


            # ==========================
            # Password Validation
            # ==========================

            if password != confirm_password:

                return self.flash_and_redirect(

                    "Passwords do not match",

                    "danger",

                    "auth.register"
                )


            # ==========================
            # Print Data in Terminal
            # ==========================

            print("\n========== USER DATA ==========")

            print("Full Name :", fullname)

            print("Email     :", email)

            print("Phone     :", phone)

            print("DOB       :", dob)

            print("PAN       :", pan)

            print("Referral  :", referral)

            print("================================\n")


            # ==========================
            # Success Message
            # ==========================

            return self.flash_and_redirect(

                "Registration Successful",

                "success",

                "auth.login"
            )


        return render_template("register.html")


    # ======================================
    # Login Page
    # ======================================

    def login(self):

        return render_template("login.html")


    # ======================================
    # Terms Page
    # ======================================

    def terms(self):

        return render_template("terms.html")



# ======================================
# Object Creation
# ======================================

auth_controller = AuthController()



# ======================================
# Routes
# ======================================

@auth.route("/")
def home():

    return render_template("register.html")



@auth.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    return auth_controller.register()



@auth.route("/login")
def login():

    return auth_controller.login()



@auth.route("/terms")
def terms():

    return auth_controller.terms()
