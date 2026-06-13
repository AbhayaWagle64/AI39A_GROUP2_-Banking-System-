import os
import sys
import html
import random
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, Response
from werkzeug.utils import secure_filename
from database_layer import db, UserProfile, Transaction, OtpVerification

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e_paisa_secure_fintech_key_2026'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "epaisa.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'avatars')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# OTP LOG FILE
OTP_LOG_FILE = os.path.join(BASE_DIR, 'otp_log.txt')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_otp(email, otp_code, otp_type="REGISTRATION"):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {otp_type} OTP for {email}: {otp_code}"
    separator = "=" * 60
    
    with open(OTP_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{separator}\n")
        f.write(f"{log_message}\n")
        f.write(f"{separator}\n\n")
    
    print(f"\n{separator}", file=sys.stderr, flush=True)
    print(f"🔐 {log_message}", file=sys.stderr, flush=True)
    print(f"{separator}\n", file=sys.stderr, flush=True)

def db_save_new_otp(email_address, secret_code):
    existing_otp = OtpVerification.query.filter_by(email=email_address).first()
    if existing_otp:
        existing_otp.otp_code = secret_code
        existing_otp.updated_at = datetime.now(timezone.utc)
    else:
        new_otp = OtpVerification(email=email_address, otp_code=secret_code)
        db.session.add(new_otp)
    db.session.commit()

# ==========================================
# CORE ROUTES (Sprint 1-3)
# ==========================================

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('register'))

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        raw_name = request.form.get('name', '').strip()
        raw_phone = request.form.get('phone', '').strip()
        raw_email = request.form.get('email', '').strip()
        raw_password = request.form.get('password')
        if not raw_name or not raw_phone or not raw_email or not raw_password:
            flash("All fields required.", "danger")
            return render_template('register.html')
        if UserProfile.query.filter((UserProfile.email == raw_email) | (UserProfile.phone == raw_phone)).first():
            flash("Email or phone exists.", "danger")
            return render_template('register.html')
        avatar = 'default_avatar.png'
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename != '' and allowed_file(file.filename):
                avatar = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S_')}{secure_filename(file.filename)}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar))
        try:
            user = UserProfile(fullname=raw_name, name=raw_name, email=raw_email, phone=raw_phone, avatar=avatar, profile_pic_path=avatar)
            user.set_password(raw_password)
            db.session.add(user)
            db.session.commit()
            session['pending_email'] = raw_email
            generated_otp = str(random.randint(100000, 999999))
            log_otp(raw_email, generated_otp, "REGISTRATION")
            db_save_new_otp(raw_email, generated_otp)
            flash("Check your OTP. (Also check otp_log.txt if terminal doesn't show it)", "success")
            return redirect(url_for('verify_otp'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "danger")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form.get('email', '').strip()
    password = request.form.get('password')
    user = UserProfile.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Invalid credentials.", "danger")
        return redirect(url_for('login'))
    if not user.is_verified:
        session['pending_email'] = user.email
        generated_otp = str(random.randint(100000, 999999))
        log_otp(user.email, generated_otp, "LOGIN_VERIFICATION")
        db_save_new_otp(user.email, generated_otp)
        flash("Account not verified. New OTP sent.", "warning")
        return redirect(url_for('verify_otp'))
    session['user_id'] = user.id
    return redirect(url_for('dashboard'))

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    pending = session.get('pending_email')
    if not pending:
        flash("Session expired.", "danger")
        return redirect(url_for('register'))
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        record = OtpVerification.query.filter_by(email=pending).first()
        if not record or record.otp_code != otp:
            flash("Invalid OTP.", "danger")
            return render_template('otp_verify.html')
        user = UserProfile.query.filter_by(email=pending).first()
        if user:
            user.is_verified = True
            txn = Transaction(id=f"TXN-{random.randint(100000, 999999)}", user_id=user.id, tx_type='credit', txn_type='credit', amount=1500.00, running_balance=1500.00, status='success', txn_status='success', reference='Welcome Bonus')
            db.session.add(txn)
            db.session.delete(record)
            db.session.commit()
            session['user_id'] = user.id
            session.pop('pending_email', None)
            return redirect(url_for('dashboard'))
        flash("User not found.", "danger")
    return render_template('otp_verify.html')

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    email = session.get('pending_email')
    if not email:
        return jsonify({"error": "Session expired"}), 400
    generated_otp = str(random.randint(100000, 999999))
    log_otp(email, generated_otp, "RESEND")
    db_save_new_otp(email, generated_otp)
    return jsonify({"success": "OTP sent.", "note": "Check terminal or otp_log.txt"})

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    return render_template("dashboard.html")

@app.route('/api/user-data', methods=['GET'])
def get_user_data():
    uid = session.get('user_id')
    if not uid:
        return jsonify({"error": "Access Denied"}), 403
    user = UserProfile.query.get(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404
    txns = []
    balance = 0.0
    for t in Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.asc()).all():
        if t.txn_type == 'credit' or t.tx_type == 'credit':
            balance += t.amount
        else:
            balance -= t.amount
        txns.append({"id": t.id, "ref": t.reference, "type": t.txn_type or t.tx_type, "amount": t.amount, "running_balance": balance, "date": t.timestamp.strftime('%a, %b %d, %Y - %I:%M %p')})
    txns.reverse()
    return jsonify({"name": user.name or user.fullname, "email": user.email, "phone": user.phone, "balance": user.balance or user.wallet_balance, "avatar": f"/static/uploads/avatars/{user.avatar or user.profile_pic_path}", "transactions": txns})

@app.route('/api/load-funds', methods=['POST'])
def load_funds():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Invalid amount"}), 400
    user = UserProfile.query.get(session['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404
    new_balance = (user.balance or user.wallet_balance) + amount
    user.balance = new_balance
    user.wallet_balance = new_balance
    txn = Transaction(id=f"TXN-{random.randint(100000, 999999)}", user_id=user.id, tx_type='credit', txn_type='credit', amount=amount, running_balance=new_balance, status='success', txn_status='success', reference='Funds Loaded')
    db.session.add(txn)
    db.session.commit()
    return jsonify({"success": "Loaded", "new_balance": new_balance})

@app.route('/api/send-money', methods=['POST'])
def send_money():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    phone = request.form.get('phone', '').strip()
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Invalid amount"}), 400
    sender = UserProfile.query.get(session['user_id'])
    if not sender or sender.phone == phone:
        return jsonify({"error": "Invalid sender"}), 400
    if (sender.balance or sender.wallet_balance) < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    recipient = UserProfile.query.filter_by(phone=phone).first()
    if not recipient:
        return jsonify({"error": "Recipient not found"}), 404
    sender_new = (sender.balance or sender.wallet_balance) - amount
    recipient_new = (recipient.balance or recipient.wallet_balance) + amount
    sender.balance = sender_new
    sender.wallet_balance = sender_new
    recipient.balance = recipient_new
    recipient.wallet_balance = recipient_new
    tid = f"TXN-{random.randint(100000, 999999)}"
    db.session.add(Transaction(id=f"{tid}-OUT", user_id=sender.id, tx_type='debit', txn_type='debit', amount=amount, running_balance=sender_new, status='success', txn_status='success', reference=recipient.name or recipient.fullname))
    db.session.add(Transaction(id=f"{tid}-IN", user_id=recipient.id, tx_type='credit', txn_type='credit', amount=amount, running_balance=recipient_new, status='success', txn_status='success', reference=sender.name or sender.fullname))
    db.session.commit()
    return jsonify({"success": "Sent", "new_balance": sender_new})

# ==========================================
# SPRINT 1-3 ENHANCED ROUTES
# ==========================================

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        session.pop('reset_token', None)
        session.pop('reset_email', None)
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = UserProfile.query.filter_by(email=email).first()
        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for('forgot_password'))
        reset_token = str(random.randint(100000, 999999))
        session['reset_email'] = email
        session['reset_token'] = reset_token
        log_otp(email, reset_token, "PASSWORD_RESET")
        flash("Reset code sent! Check terminal or otp_log.txt.", "success")
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session or 'reset_token' not in session:
        flash("Session expired.", "danger")
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        new_password = request.form.get('new_password', '')
        if token != session.get('reset_token'):
            flash("Invalid reset code.", "danger")
            return redirect(url_for('reset_password'))
        user = UserProfile.query.filter_by(email=session['reset_email']).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            session.pop('reset_email', None)
            session.pop('reset_token', None)
            flash("Password updated! Login now.", "success")
            return redirect(url_for('login'))
        flash("User not found.", "danger")
    return render_template('reset_password.html', email=session.get('reset_email', ''))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    user = UserProfile.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('login'))
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'update_profile':
            new_name = request.form.get('name', '').strip()
            new_phone = request.form.get('phone', '').strip()
            if new_name:
                user.name = new_name
                user.fullname = new_name
            if new_phone:
                user.phone = new_phone
            if 'avatar' in request.files:
                file = request.files['avatar']
                if file and file.filename != '' and allowed_file(file.filename):
                    avatar = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S_')}{secure_filename(file.filename)}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar))
                    user.avatar = avatar
                    user.profile_pic_path = avatar
            db.session.commit()
            flash("Profile updated!", "success")
        elif action == 'change_password':
            current = request.form.get('current_password', '')
            new_pass = request.form.get('new_password', '')
            if not user.check_password(current):
                flash("Current password incorrect.", "danger")
            elif len(new_pass) < 8:
                flash("Password must be 8+ characters.", "danger")
            else:
                user.set_password(new_pass)
                db.session.commit()
                flash("Password changed!", "success")
        return redirect(url_for('profile'))
    transaction_count = Transaction.query.filter_by(user_id=user.id).count()
    return render_template('profile.html', user=user, transaction_count=transaction_count)

@app.route('/transaction/<txn_id>')
def transaction_confirmation(txn_id):
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    txn = Transaction.query.filter_by(id=txn_id).first()
    if not txn or txn.user_id != session['user_id']:
        flash("Transaction not found.", "danger")
        return redirect(url_for('dashboard'))
    return render_template('confirmation.html', txn=txn)

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    user = UserProfile.query.get(session['user_id'])
    if not user or user.email != 'admin@epaisa.com':
        flash("Admin access required.", "danger")
        return redirect(url_for('dashboard'))
    users = UserProfile.query.all()
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    stats = {
        'total_users': UserProfile.query.count(),
        'total_transactions': Transaction.query.count(),
        'total_volume': db.session.query(db.func.sum(Transaction.amount)).scalar() or 0,
        'verified_users': UserProfile.query.filter_by(is_verified=True).count()
    }
    return render_template('admin.html', users=users, transactions=transactions, stats=stats)

@app.route('/admin/export/users')
def export_users():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    users = UserProfile.query.all()
    csv = "ID,Name,Email,Phone,Balance,Verified\n"
    for u in users:
        csv += f"{u.id},{u.name or u.fullname},{u.email},{u.phone},{u.balance or u.wallet_balance},{u.is_verified}\n"
    return Response(csv, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=users.csv"})

@app.route('/admin/export/transactions')
def export_transactions():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    txns = Transaction.query.all()
    csv = "ID,User,Type,Amount,Balance,Reference,Date\n"
    for t in txns:
        csv += f"{t.id},{t.user_id},{t.txn_type or t.tx_type},{t.amount},{t.running_balance},{t.reference},{t.timestamp}\n"
    return Response(csv, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=transactions.csv"})

# ==========================================
# SPRINT 4 ROUTES (NEW)
# ==========================================

@app.route('/qr-payment')
def qr_payment():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    return render_template('qr_payment.html')

@app.route('/merchant-payment')
def merchant_payment():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    return render_template('merchant_payment.html')

@app.route('/utility-payment')
def utility_payment():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    return render_template('utility_payment.html')

@app.route('/mobile-recharge')
def mobile_recharge():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    return render_template('mobile_recharge.html')

@app.route('/saved-payments')
def saved_payments():
    if 'user_id' not in session:
        flash("Login required.", "danger")
        return redirect(url_for('login'))
    return render_template('saved_payments.html')

# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    if 'user_id' in session:
        return render_template('404.html'), 404
    return redirect(url_for('login'))

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ==========================================
# START SERVER
# ==========================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)