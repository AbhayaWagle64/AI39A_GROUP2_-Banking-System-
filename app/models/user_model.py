# app/models/user_model.py
from app.extensions import db

class UserModel(db.Model):
    __tablename__ = 'users'

    # Defining the columns to match your database schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    @staticmethod
    def get_profile_by_id(user_id):
        """Fetches user profile data from the database using SQLAlchemy."""
        user = UserModel.query.get(user_id)
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone
            }
        return None

    @staticmethod
    def update_profile_by_id(user_id, email, phone):
        """Updates user profile details in the database using SQLAlchemy."""
        user = UserModel.query.get(user_id)
        if user:
            try:
                user.email = email
                user.phone = phone
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Database Error during profile update: {e}")
                return False
        return False