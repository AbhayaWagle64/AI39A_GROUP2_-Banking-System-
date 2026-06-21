from flask import flash, render_template, request

from app.controllers.receive_money_controller import ReceiveMoneyController


def show_wallet():
    return render_template("wallet/wallet.html")


def show_wallet_summary():
    return render_template("wallet/summary.html")


def show_add_money():
    return render_template("wallet/add_money.html")


def show_withdraw_money():
    return render_template("wallet/withdraw_money.html")


def show_linked_accounts():
    return render_template("wallet/linked_accounts.html")


def send_money():
    if request.method == "POST":
        receiver = request.form.get("receiver", "").strip()
        amount = request.form.get("amount", "").strip()
        remarks = request.form.get("remarks", "").strip()

        if not receiver or not amount:
            flash("Receiver and amount are required.", "danger")
            return render_template("send_money.html")

        try:
            amount_value = float(amount)
            if amount_value <= 0:
                raise ValueError
        except ValueError:
            flash("Enter a valid amount greater than zero.", "danger")
            return render_template("send_money.html")

        flash(f"Money transfer of Rs. {amount_value:.2f} to {receiver} is ready for confirmation.", "success")
        return render_template(
            "wallet/transaction_confirmation.html",
            receiver=receiver,
            amount=amount_value,
            remarks=remarks,
        )

    return render_template("send_money.html")


def receive_money():
    return ReceiveMoneyController.receive_money()
