from flask import render_template, request, flash, session

class ReceiveMoneyController:

 @staticmethod
 def receive_money():

    if request.method == "POST":

        sender_email = request.form.get("sender_email")
        amount = request.form.get("amount")

        if not sender_email:
            flash("Sender email is required.", "danger")
            return render_template("receive_money.html")

        if not amount:
            flash("Amount is required.", "danger")
            return render_template("receive_money.html")

        try:
            amount = float(amount)

            if amount <= 0:
                flash("Amount must be greater than zero.", "danger")
                return render_template("receive_money.html")

        except ValueError:
            flash("Invalid amount.", "danger")
            return render_template("receive_money.html")

        # Future database logic goes here

        flash(
            f"Payment request of Rs. {amount:.2f} sent to {sender_email}",
            "success"
        )

    return render_template("receive_money.html")

