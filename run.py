import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e_paisa_secret_key'

# ==========================================
# DATABASE SETUPS
# ==========================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "epaisa.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Profile Picture upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'avatars')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limit file uploads to 5MB

# Automatically make the avatar storage directories if they do not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the database engine
db = SQLAlchemy(app)


# ==========================================
# DATABASE MODELS / BLUEPRINTS
# ==========================================

# Database Blueprint (Schema) for storing user profiles and bank balances
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    profile_pic_path = db.Column(db.String(255), nullable=True)  # Added for US #4
    wallet_balance = db.Column(db.Float, default=0.0)             # Added for US #7

# --- USER STORY #12 (DATABASE): BAIBHAV'S OTP TABLE STRUCTURE ---
class UserOTP(db.Model):
    """
    DATABASE LAYER: Stores temporary security verification codes
    linked to an email profile to validate operational actions.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)


# Helper utility function to validate file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =======================================================
# DATABASE LAYER DATA-ACCESS FUNCTIONS
# =======================================================

# --- USER STORY #7 (DATABASE) ---
def get_user_balance_from_db(user_email):
    """
    DATABASE LAYER: Queries the epaisa.db file to look up a 
    specific user account record and return their numeric balance.
    """
    user_record = UserProfile.query.filter_by(email=user_email).first()
    if user_record:
        return {
            "exists": True,
            "fullname": user_record.fullname,
            "balance": user_record.wallet_balance
        }
    return {"exists": False, "balance": 0.0}


# --- USER STORY #12 (DATABASE): BAIBHAV'S QUERY UTILITIES ---
def db_save_new_otp(email, code):
    """
    DATABASE LAYER: Persists a newly created verification token.
    Clears previous entries associated with the email to prevent spam.
    """
    UserOTP.query.filter_by(user_email=email).delete()
    new_otp = UserOTP(user_email=email, otp_code=str(code), is_verified=False)
    db.session.add(new_otp)
    db.session.commit()
    return True

def db_verify_otp_match(email, code_to_check):
    """
    DATABASE LAYER: Scans unverified data elements to match verification tokens.
    Deactivates tokens instantly upon a match to avoid duplicate entry exploits.
    """
    record = UserOTP.query.filter_by(user_email=email, otp_code=str(code_to_check), is_verified=False).first()
    if record:
        record.is_verified = True
        db.session.commit()
        return True
    return False


# ==========================================
# APPLICATION ROUTES & API GATEWAYS
# ==========================================

@app.route("/")
def home():
    return redirect(url_for("register"))


# --- USER STORY #13 (BACKEND): FLASH ALERT MODIFICATIONS BY BAIBHAV ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")

        print(fullname, email, phone)
        
        # Check validation states
        if UserProfile.query.filter_by(email=email).first():
            flash("Registration Failed: This email address is already registered.", "danger")
            return redirect(url_for("register"))
            
        new_user = UserProfile(fullname=fullname, email=email, phone=phone, wallet_balance=5000.0)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Welcome {fullname}! Your account has been generated with a 5000 NPR testing bonus.", "success")
        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/login")
def login():
    return "Login Page"


# --- USER STORY #4: PROFILE MANAGEMENT (BACKEND) ---
@app.route("/profile/upload-avatar", methods=["POST"])
def upload_avatar():
    user = UserProfile.query.first()
    if not user:
        return jsonify({"status": "error", "message": "No registered users found to attach image to."}), 404

    if 'profile_pic' not in request.files:
        return jsonify({"status": "error", "message": "No profile_pic form-data boundary found."}), 400
        
    file = request.files['profile_pic']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Empty file field submitted."}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"user_{user.id}_{filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        if user.profile_pic_path and os.path.exists(user.profile_pic_path):
            try:
                os.remove(user.profile_pic_path)
            except Exception:
                pass 
                
        file.save(save_path)
        user.profile_pic_path = os.path.join('static', 'uploads', 'avatars', unique_filename)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Profile picture updated successfully!",
            "database_saved_path": user.profile_pic_path
        }), 200

    return jsonify({"status": "error", "message": "File validation rejected. Only PNG, JPG, JPEG, or WebP allowed."}), 400


# --- USER STORY #7: CHECK WALLET BALANCE ---
@app.route("/api/wallet/balance", methods=["GET"])
def check_balance():
    user_email = request.args.get('email')
    if not user_email:
        return jsonify({"status": "error", "message": "Missing 'email' query parameter."}), 400
        
    db_result = get_user_balance_from_db(user_email)
    if not db_result["exists"]:
        return jsonify({"status": "error", "message": f"No account found matching email: {user_email}"}), 404
        
    currency = "NPR"
    return jsonify({
        "status": "success",
        "fullname": db_result["fullname"],
        "raw_balance": db_result["balance"],
        "formatted_balance": f"{currency} {db_result['balance']:,.2f}"
    }), 200


# --- USER STORY #12 & #13 (BACKEND): BAIBHAV'S STATUS TERMINATION ROUTE ---
@app.route("/api/security/verify-otp", methods=["POST"])
def handle_otp_verification():
    """
    BACKEND ENDPOINT: Validates credentials and passes clean success/error 
    JSON message definitions up to frontend UI layout components.
    """
    data = request.get_json() or {}
    email = data.get("email")
    submitted_code = data.get("otp")
    
    if not email or not submitted_code:
        return jsonify({"status": "error", "message": "Verification rejected. Email and OTP token required."}), 400
        
    # Process against Baibhav's database check utility
    is_valid = db_verify_otp_match(email, submitted_code)
    
    if is_valid:
        return jsonify({"status": "success", "message": "Security code confirmed! Context unlocked successfully."}), 200
    
    return jsonify({"status": "error", "message": "Invalid, missing, or expired verification token. Access denied."}), 401


# --- USER STORY #11: DASHBOARD VIEW ---
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ==========================================
# AUTO-INITIALIZE SCHEMAS ON SERVER STARTUP
# ==========================================
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)