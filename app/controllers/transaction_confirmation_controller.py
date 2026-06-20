from flask import render_template, session, flash

from app.database import Database


class TransactionController:

    @staticmethod
    def transaction_history():

        db = Database()

        try:

            user = db.fetch_one(
                """
                SELECT email, epaisa_id
                FROM register
                WHERE username = %s
                """,
                (session["username"],)
            )

            if not user:
                flash("User not found.", "danger")
                return render_template(
                    "transactions/transactions.html",
                    transactions=[]
                )

            transactions = db.fetch_all(
                """
                SELECT *
                FROM transactions
                WHERE sender_email = %s
                   OR receiver_email = %s
                   OR sender_epaisa_id = %s
                   OR receiver_epaisa_id = %s
                ORDER BY transaction_date DESC
                """,
                (
                    user["email"],
                    user["email"],
                    user["epaisa_id"],
                    user["epaisa_id"]
                )
            )

            db.close()

            return render_template(
                "transactions/transactions.html",
                transactions=transactions
            )

        except Exception as e:

            db.close()

            flash(str(e), "danger")

            return render_template(
                "transactions/transactions.html",
                transactions=[]
            )


    @staticmethod
    def transaction_details(transaction_id):

        db = Database()

        try:

            transaction = db.fetch_one(
                """
                SELECT *
                FROM transactions
                WHERE id = %s
                """,
                (transaction_id,)
            )

            db.close()

            if not transaction:
                flash("Transaction not found.", "danger")

                return render_template(
                    "transactions/transaction_details.html",
                    transaction=None
                )

            return render_template(
                "transactions/transaction_details.html",
                transaction=transaction
            )

        except Exception as e:

            db.close()

            flash(str(e), "danger")

            return render_template(
                "transactions/transaction_details.html",
                transaction=None
            )


    @staticmethod
    def recent_transactions(limit=5):

        db = Database()

        try:

            user = db.fetch_one(
                """
                SELECT email, epaisa_id
                FROM register
                WHERE username = %s
                """,
                (session["username"],)
            )

            transactions = db.fetch_all(
                f"""
                SELECT *
                FROM transactions
                WHERE sender_email = %s
                   OR receiver_email = %s
                   OR sender_epaisa_id = %s
                   OR receiver_epaisa_id = %s
                ORDER BY transaction_date DESC
                LIMIT {limit}
                """,
                (
                    user["email"],
                    user["email"],
                    user["epaisa_id"],
                    user["epaisa_id"]
                )
            )

            db.close()

            return transactions

        except Exception:

            db.close()

            return []