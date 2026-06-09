from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import random

class TransactionOTPRoutes:
    def register(self):
        transaction_otp_bp = Blueprint('transaction_otp', __name__)

        @transaction_otp_bp.route('/transaction-otp')
        def transaction_otp():
            amount = request.args.get('amount', '0.00')
            # Generate OTP
            otp = random.randint(100000, 999999)
            session['transaction_otp'] = str(otp)
            session['transaction_amount'] = amount
            flash(f'Your OTP is: {otp}', 'success')
            return render_template('transaction_otp.html', amount=amount)

        @transaction_otp_bp.route('/verify-transaction-otp', methods=['POST'])
        def verify_transaction_otp():
            entered_otp = request.form.get('otp')
            if entered_otp == session.get('transaction_otp'):
                session.pop('transaction_otp', None)
                flash('Transaction verified successfully!', 'success')
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Invalid OTP. Please try again.', 'danger')
                return redirect(url_for('transaction_otp.transaction_otp'))

        @transaction_otp_bp.route('/resend-transaction-otp')
        def resend_transaction_otp():
            otp = random.randint(100000, 999999)
            session['transaction_otp'] = str(otp)
            flash(f'New OTP sent! Your OTP is: {otp}', 'success')
            return redirect(url_for('transaction_otp.transaction_otp'))

        return transaction_otp_bp