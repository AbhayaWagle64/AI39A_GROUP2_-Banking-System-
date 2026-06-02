from flask_sqlalchemy import SQLAlchemy

# 1. Initialize database globally so it can be cleanly imported across files
db = SQLAlchemy()

# 2. Your Database Table Blueprint (Schema)
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    profile_pic_path = db.Column(db.String(255), nullable=True)
    wallet_balance = db.Column(db.Float, default=0.0)


# =======================================================
# DATABASE LAYER DATA-ACCESS FUNCTIONS (User Story #7)
# =======================================================

def get_user_balance_from_db(user_email):
    """
    DATABASE LAYER: Queries the epaisa.db file to look up a 
    specific user account record and return their numeric balance.
    """
    # Look up the user row in the database by their unique email address
    user_record = UserProfile.query.filter_by(email=user_email).first()
    
    if user_record:
        # Return the raw numeric value directly from the SQL database row
        return {
            "exists": True,
            "fullname": user_record.fullname,
            "balance": user_record.wallet_balance
        }
    
    # Return false if no row matches the query criteria
    return {"exists": False, "balance": 0.0}