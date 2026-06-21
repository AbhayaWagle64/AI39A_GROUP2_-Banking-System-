from flask import flash, render_template, request


def reports():
    return render_template("report_wrong_transaction.html")


def report_wrong_transaction():
    if request.method == "POST":
        transaction_id = request.form.get("transaction_id", "").strip()
        reason = request.form.get("reason", "").strip()
        description = request.form.get("description", "").strip()

        if not transaction_id or not reason:
            flash("Transaction ID and reason are required.", "danger")
            return render_template("report_wrong_transaction.html")

        flash("Report submitted successfully. Our support team will review it.", "success")
        return render_template("report_wrong_transaction.html")

    return render_template("report_wrong_transaction.html")
