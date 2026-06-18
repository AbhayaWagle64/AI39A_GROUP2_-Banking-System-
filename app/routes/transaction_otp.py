from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from app import mail
import random
import mysql.connector
from datetime import datetime, timedelta

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='epaisa'
    )

class TransactionOTPRoutes:
    def register(self):
        transaction_otp_bp = Blueprint('transaction_otp', __name__)

        @transaction_otp_bp.route('/transaction-otp')
        def transaction_otp():
            amount = request.args.get('amount', '0.00')
            receiver_id = request.args.get('receiver_id')

            if not session.get('user_id'):
                flash('Please login first.', 'danger')
                return redirect(url_for('auth.login'))

            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Save OTP to database
            db = get_db()
            cursor = db.cursor()
            expires_at = datetime.now() + timedelta(minutes=5)

            # Delete any old unused OTPs for this user
            cursor.execute(
                "DELETE FROM otp_verifications WHERE user_id = %s AND is_used = 0",
                (session['user_id'],)
            )

            # Insert new OTP
            cursor.execute("""
                INSERT INTO otp_verifications
                (user_id, otp, amount, receiver_id, expires_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (session['user_id'], otp, float(amount), receiver_id, expires_at))
            db.commit()

            # Get user email
            cursor.execute(
                "SELECT email, fullname FROM users WHERE id = %s",
                (session['user_id'],)
            )
            user = cursor.fetchone()
            cursor.close()
            db.close()

            # Send OTP via email
            if user:
                try:
                    msg = Message(
                        subject='ePaisa Transaction OTP',
                        recipients=[user[0]]
                    )
                    msg.body = f"""
Hello {user[1]},

Your OTP for the transaction of Rs. {amount} is:

{otp}

This OTP is valid for 5 minutes.
Do not share this OTP with anyone.

— ePaisa Team
                    """
                    mail.send(msg)
                    flash('OTP sent to your registered email.', 'success')
                except Exception as e:
                    # Fallback: show OTP in flash if email fails
                    flash(f'Email failed. Your OTP is: {otp}', 'warning')

            # Store in session as backup
            session['transaction_otp'] = otp
            session['transaction_amount'] = amount
            session['transaction_receiver_id'] = receiver_id

            return render_template('transaction_otp.html', amount=amount)

        @transaction_otp_bp.route('/verify-transaction-otp', methods=['POST'])
        def verify_transaction_otp():
            entered_otp = request.form.get('otp')

            if not session.get('user_id'):
                flash('Please login first.', 'danger')
                return redirect(url_for('auth.login'))

            db = get_db()
            cursor = db.cursor(dictionary=True)

            # Check OTP in database
            cursor.execute("""
                SELECT * FROM otp_verifications
                WHERE user_id = %s
                AND otp = %s
                AND is_used = 0
                AND expires_at > NOW()
                ORDER BY created_at DESC
                LIMIT 1
            """, (session['user_id'], entered_otp))

            otp_record = cursor.fetchone()

            if not otp_record:
                flash('Invalid or expired OTP. Please try again.', 'danger')
                cursor.close()
                db.close()
                amount = session.get('transaction_amount', '0.00')
                return render_template('transaction_otp.html', amount=amount)

            # OTP is valid — complete the transaction
            amount = otp_record['amount']
            receiver_id = otp_record['receiver_id']
            sender_id = session['user_id']

            try:
                # Deduct from sender
                cursor.execute(
                    "UPDATE wallet SET balance = balance - %s WHERE user_id = %s",
                    (amount, sender_id)
                )

                # Add to receiver
                cursor.execute(
                    "UPDATE wallet SET balance = balance + %s WHERE user_id = %s",
                    (amount, receiver_id)
                )

                # Record transaction
                cursor.execute("""
                    INSERT INTO transactions
                    (sender_id, receiver_id, amount, title, type, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (sender_id, receiver_id, amount,
                      'Money Transfer', 'transfer', 'completed'))

                # Mark OTP as used
                cursor.execute(
                    "UPDATE otp_verifications SET is_used = 1 WHERE id = %s",
                    (otp_record['id'],)
                )

                db.commit()

                # Clear session data
                session.pop('transaction_otp', None)
                session.pop('transaction_amount', None)
                session.pop('transaction_receiver_id', None)

                flash(f'Transaction of Rs. {amount} completed successfully!', 'success')
                return redirect(url_for('dashboard.dashboard'))

            except Exception as e:
                db.rollback()
                flash('Transaction failed. Please try again.', 'danger')
                return render_template('transaction_otp.html', amount=amount)

            finally:
                cursor.close()
                db.close()

        @transaction_otp_bp.route('/resend-transaction-otp')
        def resend_transaction_otp():
            amount = session.get('transaction_amount', '0.00')
            receiver_id = session.get('transaction_receiver_id')
            return redirect(url_for(
                'transaction_otp.transaction_otp',
                amount=amount,
                receiver_id=receiver_id
            ))

        return transaction_otp_bp