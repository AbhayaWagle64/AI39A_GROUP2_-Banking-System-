from flask import flash, render_template, request


def show_qr_payment():
    return render_template("qr_payment.html")


def qr_payment():
    receiver_id = request.form.get("receiver_id", "").strip()
    amount = request.form.get("amount", "").strip()

    if not receiver_id or not amount:
        flash("Recipient ID and amount are required.", "danger")
        return render_template("qr_payment.html")

    try:
        amount_value = float(amount)
        if amount_value <= 0:
            raise ValueError
    except ValueError:
        flash("Enter a valid amount greater than zero.", "danger")
        return render_template("qr_payment.html")

    flash(f"QR payment of Rs. {amount_value:.2f} to {receiver_id} is ready.", "success")
    return render_template(
        "wallet/transaction_confirmation.html",
        receiver=receiver_id,
        amount=amount_value,
    )
