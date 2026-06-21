from flask import render_template, request, redirect, session

from app.controllers.auth_controller import AuthController
from app.controllers.wallet_controller import WalletController
from app.controllers.transaction_controller import TransactionController
from app.controllers.otp_controller import OTPController
from app.controllers.admin_controller import AdminController
from app.controllers.bill_controller import BillController
from app.controllers.report_controller import ReportController
from app.database import get_connection


def init_routes(app):

    # ---------------- HOME ----------------
    @app.route("/")
    def home():
        return redirect("/login")

    # ---------------- REGISTER ----------------
    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":

            data = request.form

            result = AuthController.register(
                data["name"],
                data["phone"],
                data["email"],
                data["password"]
            )

            if not result.get("success"):
                return render_template(
                    "register.html",
                    error=result.get("message")
                )

            # Auto-login after registration
            session["user"] = result.get("wallet_id")

            return redirect("/dashboard")

        return render_template("register.html")

    # ---------------- FORGOT / RESET / OTP PAGES ----------------
    @app.route("/forgot-password")
    def forgot_password():
        return render_template("forgot_password.html")

    @app.route("/reset-password")
    def reset_password():
        return render_template("reset_password.html")

    @app.route("/otp-verification")
    def otp_verification():
        return render_template("otp_verification.html")

    # ---------------- OTHER PAGES ----------------
    @app.route("/recieve-money")
    def recieve_money():
        return render_template("recieve_money.html")

    @app.route("/notifications")
    def notifications():
        return render_template("notifications.html")

    @app.route('/transaction-confirmation')
    def transaction_confirmation():
        return render_template('transaction_confirmation.html')

    @app.route('/reports')
    def reports_page():
        return render_template('reports.html')

    # ---------------- LOGIN ----------------
    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            data = request.form

            result = AuthController.login(
                data["phone"],
                data["password"]
            )

            if not result.get("success"):
                # show message on the login page
                return render_template("login.html", error=result.get("message"))

            # Successful login: set session and redirect to dashboard
            session["user"] = result.get("wallet_id")
            return redirect("/dashboard")

        return render_template("login.html")

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        return redirect('/login')

    # ---------------- DASHBOARD ----------------
    @app.route("/dashboard")
    def dashboard():

        if "user" not in session:
            return redirect("/login")

        wallet_id = session["user"]

        wallet = WalletController.get_dashboard(wallet_id)

        return render_template(
            "dashboard.html",
            wallet=wallet
        )

    # ---------------- CREATE TRANSACTION ----------------
    @app.route("/create-transaction", methods=["POST"])
    def create_transaction():

        data = request.form

        result = TransactionController.create(
            data["sender_wallet"],
            data["receiver_wallet"],
            float(data["amount"])
        )

        if not result["success"]:
            return result["message"]

        otp = OTPController.generate(
            result["transaction_id"]
        )

        return f"OTP Generated: {otp}"

    # ---------------- VERIFY OTP ----------------
    @app.route("/verify-otp", methods=["POST"])
    def verify_otp():

        data = request.form

        valid = OTPController.verify(
            data["transaction_id"],
            data["otp"]
        )

        if not valid:
            return "Invalid or Expired OTP"

        TransactionController.complete(
            data["transaction_id"]
        )

        return render_template(
            "transaction_success.html"
        )

    # ---------------- ADMIN ----------------
    @app.route("/admin/transactions")
    def admin_transactions():

        data = AdminController.get_all_transactions()

        return render_template(
            "admin/transactions.html",
            transactions=data
        )

    # ---------------- BILL PAYMENT ----------------
    @app.route("/pay-bill", methods=["GET", "POST"])
    def pay_bill():

        if request.method == "POST":

            data = request.form

            BillController.pay_bill(
                session.get("user_id"),
                data["bill_type"],
                data["customer_id"],
                float(data["amount"])
            )

            return "Bill Paid Successfully"

        return render_template("bill_payment.html")

    # ---------------- REPORT ----------------
    @app.route("/report")
    def report():

        file = ReportController.generate_csv()

        return f"Report generated: {file}"
