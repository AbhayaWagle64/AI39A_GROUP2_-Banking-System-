from flask import Blueprint, render_template, request, redirect, url_for, flash

class MobileRechargeRoutes:
    def register(self):
        mobile_recharge_bp = Blueprint('mobile_recharge', __name__)

        @mobile_recharge_bp.route('/mobile-recharge', methods=['GET'])
        def mobile_recharge():
            return render_template('mobile_recharge.html')

        @mobile_recharge_bp.route('/mobile-recharge', methods=['POST'])
        def process_recharge():
            mobile_number = request.form.get('mobile_number')
            operator = request.form.get('operator')
            amount = request.form.get('amount')
            payment_method = request.form.get('payment_method')

            # Validation
            if not mobile_number or len(mobile_number) != 10:
                flash('Please enter a valid 10-digit mobile number.', 'danger')
                return redirect(url_for('mobile_recharge.mobile_recharge'))

            if not operator:
                flash('Please select an operator (Ncell or NTC).', 'danger')
                return redirect(url_for('mobile_recharge.mobile_recharge'))

            if not amount or float(amount) < 10:
                flash('Please select or enter a valid recharge amount.', 'danger')
                return redirect(url_for('mobile_recharge.mobile_recharge'))

            if not payment_method:
                flash('Please select a payment method.', 'danger')
                return redirect(url_for('mobile_recharge.mobile_recharge'))

            # Success
            flash(f'✅ Rs. {amount} recharge successful for {mobile_number} ({operator}) via {payment_method}!', 'success')
            return redirect(url_for('mobile_recharge.mobile_recharge'))

        return mobile_recharge_bp