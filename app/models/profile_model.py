# models/profile_model.py
from config.db_config import get_db_connection

class ProfileModel:

    @staticmethod
    def get_profile_by_id(user_id):
        """Fetches user profile data from the database using the User ID."""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # dictionary=True makes it easy to read column names
        
        # Select only profile details, exclude passwords for security
        query = "SELECT username, email, phone FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_profile = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return user_profile

    @staticmethod
    def update_profile_by_id(user_id, email, phone):
        """Updates user profile details in the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "UPDATE users SET email = %s, phone = %s WHERE id = %s"
        try:
            cursor.execute(query, (email, phone, user_id))
            conn.commit()
            return cursor.rowcount > 0 # Returns True if a row was updated
        except Exception as e:
            print(f"Database Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()