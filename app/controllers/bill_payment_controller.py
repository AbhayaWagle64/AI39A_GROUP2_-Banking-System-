from flask import flash, render_template, request


def bill_payment():
    if request.method == "POST":
        biller = request.form.get("biller", "").strip()
        amount = request.form.get("amount", "").strip()

        if not biller or not amount:
            flash("Biller and amount are required.", "danger")
            return render_template("bill_payment.html")

        flash(f"Bill payment request for {biller} is ready.", "success")
        return render_template("bill_payment.html")

    return render_template("bill_payment.html")
