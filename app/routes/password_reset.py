from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import random

class PasswordResetRoutes:
    def register(self):
        password_reset_bp = Blueprint('password_reset', __name__)

        @password_reset_bp.route('/forgot-password', methods=['GET', 'POST'])
        def forgot_password():
            if request.method == 'POST':
                identifier = request.form.get('identifier')

                # Check if identifier is empty
                if not identifier:
                    flash('Please enter your email or mobile number.')
                    return redirect(url_for('password_reset.forgot_password'))

                # Generate a 6-digit OTP
                otp = random.randint(100000, 999999)

                # Store OTP and identifier in session
                session['otp'] = str(otp)
                session['identifier'] = identifier

                # In real app, send OTP via email/SMS
                # For now we flash it so you can test
                flash(f'OTP sent to {identifier}. Your OTP is: {otp}')
                return redirect(url_for('password_reset.verify_otp'))

            return render_template('auth/forgot_password.html')

        @password_reset_bp.route('/verify-otp', methods=['GET', 'POST'])
        def verify_otp():
            if request.method == 'POST':
                entered_otp = request.form.get('otp')

                if entered_otp == session.get('otp'):
                    flash('OTP verified! Please enter your new password.')
                    return redirect(url_for('password_reset.reset_password'))
                else:
                    flash('Invalid OTP. Please try again.')
                    return redirect(url_for('password_reset.verify_otp'))

            return render_template('auth/verify_otp.html')

        @password_reset_bp.route('/reset-password', methods=['GET', 'POST'])
        def reset_password():
            if request.method == 'POST':
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')

                # Check if passwords match
                if new_password != confirm_password:
                    flash('Passwords do not match. Please try again.')
                    return redirect(url_for('password_reset.reset_password'))

                # Check password length
                if len(new_password) < 6:
                    flash('Password must be at least 6 characters.')
                    return redirect(url_for('password_reset.reset_password'))

                # In real app, update password in database here
                # For now just flash success
                session.pop('otp', None)
                session.pop('identifier', None)
                flash('Password reset successful! Please login with your new password.')
                return redirect(url_for('dashboard.dashboard'))

            return render_template('auth/reset_password.html')

        return password_reset_bp