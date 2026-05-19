# app/models/user_model.py
from config.db_config import get_db_connection

class UserModel:

    @staticmethod
    def get_profile_by_id(user_id):
        """Fetches user profile data from the database using the User ID."""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # returns rows as a dictionary
        
        # Select profile details, excluding passwords for security
        query = "SELECT id, username, email, phone FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_profile = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return user_profile

    @staticmethod
    def update_profile_by_id(user_id, email, phone):
        """Updates user profile details (email and phone) in the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "UPDATE users SET email = %s, phone = %s WHERE id = %s"
        try:
            cursor.execute(query, (email, phone, user_id))
            conn.commit()
            return cursor.rowcount > 0 # Returns True if the profile was successfully updated
        except Exception as e:
            print(f"Database Error during profile update: {e}")
            return False
        finally:
            cursor.close()
            conn.close()