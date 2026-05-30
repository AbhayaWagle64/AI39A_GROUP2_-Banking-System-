from flask import Blueprint, render_template, request, redirect, url_for, flash

class WalletRoutes:
    def register(self):
        wallet_bp = Blueprint('wallet', __name__)

        @wallet_bp.route('/wallet')
        def wallet():
            balance = 1000.00
            return render_template('wallet.html', balance=balance)

        @wallet_bp.route('/wallet/add', methods=['POST'])
        def add_money():
            amount = request.form.get('amount')
            method = request.form.get('method')
            flash(f'Rs. {amount} added successfully!', 'success')
            return redirect(url_for('wallet.wallet'))

        @wallet_bp.route('/wallet/withdraw', methods=['POST'])
        def withdraw_money():
            amount = request.form.get('amount')
            destination = request.form.get('destination')
            flash(f'Rs. {amount} withdrawn to {destination} successfully!', 'success')
            return redirect(url_for('wallet.wallet'))

        return wallet_bp