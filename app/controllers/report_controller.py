import csv

from app.database import get_connection


class ReportController:

    @staticmethod
    def generate_csv():

        conn = get_connection()

        data = conn.execute(
            "SELECT * FROM transactions"
        ).fetchall()

        filename = "report.csv"

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Sender",
                "Receiver",
                "Amount",
                "Status",
                "Date"
            ])

            for row in data:

                writer.writerow([
                    row["sender_wallet"],
                    row["receiver_wallet"],
                    row["amount"],
                    row["status"],
                    row["created_at"]
                ])

        conn.close()

        return filename
