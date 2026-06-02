from flask import Blueprint, render_template

class MiniStatementRoutes:
    def register(self):
        mini_bp = Blueprint('mini_statement', __name__)

        @mini_bp.route('/mini-statement')
        def mini_statement():
            balance = 1000.00

            # Temporary sample transactions
            # Backend (Abhaya) will replace with real database data
            transactions = [
                {'id': 1, 'title': 'Money Added', 'date': '2026-06-02', 'amount': 500, 'type': 'credit'},
                {'id': 2, 'title': 'Withdrawal', 'date': '2026-06-01', 'amount': 200, 'type': 'debit'},
                {'id': 3, 'title': 'Money Added', 'date': '2026-05-30', 'amount': 1000, 'type': 'credit'},
            ]

            return render_template('mini_statement.html',
                                   balance=balance,
                                   transactions=transactions)

        return mini_bp