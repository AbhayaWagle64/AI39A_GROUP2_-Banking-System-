import sqlite3

DATABASE_NAME = "epaisa.db"


class Database:
    def __init__(self):
        self.__connection = sqlite3.connect(DATABASE_NAME)
        self.__connection.row_factory = sqlite3.Row

    def fetch_one(self, query, params=None):
        cursor = self.__connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None

    def fetch_all(self, query, params=None):
        cursor = self.__connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return [dict(row) for row in results]

    def execute(self, query, params=None):
        cursor = self.__connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.__connection.commit()
        cursor.close()

    def close(self):
        self.__connection.close()

    @staticmethod
    def create_tables():
        db = Database()
        
        try:
            db.execute("""
                CREATE TABLE IF NOT EXISTS administration (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
        except Exception as e:
            print(f"Error creating administration table: {e}")

        try:
            db.execute("""
                CREATE TABLE IF NOT EXISTS register (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL,
                    customer_id TEXT UNIQUE,
                    epaisa_id TEXT UNIQUE NOT NULL,
                    balance REAL DEFAULT 0.00,
                    address TEXT,
                    account_type TEXT DEFAULT 'Savings',
                    date_joined TEXT DEFAULT '2026-01-01'
                )
            """)
        except Exception as e:
            print(f"Error creating register table: {e}")

        try:
            db.execute("""
                CREATE TABLE IF NOT EXISTS login (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    epaisa_id TEXT
                )
            """)
        except Exception as e:
            print(f"Error creating login table: {e}")

        try:
            db.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_email TEXT,
                    sender_epaisa_id TEXT,
                    receiver_email TEXT,
                    receiver_epaisa_id TEXT,
                    amount REAL,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'completed'
                )
            """)
        except Exception as e:
            print(f"Error creating transactions table: {e}")

        # Insert default admin users
        try:
            from werkzeug.security import generate_password_hash
            for admin_email, admin_password in [('admin@admin.com', 'Admin#AW64'), ('admin1@admin.com', 'Admin1#AW64')]:
                existing = db.fetch_one("SELECT * FROM administration WHERE admin_email = ?", (admin_email,))
                if not existing:
                    db.execute(
                        "INSERT INTO administration (admin_email, password) VALUES (?, ?)",
                        (admin_email, generate_password_hash(admin_password))
                    )
        except Exception as e:
            print(f"Error creating admin users: {e}")

        # SQLite-specific column additions (if needed for migration)
        try:
            # Check and add missing columns for register table
            register_columns = db.fetch_all("PRAGMA table_info(register)")
            register_col_names = {col['name'] for col in register_columns}
            
            required_columns = {
                "epaisa_id": "TEXT",
                "customer_id": "TEXT",
                "balance": "REAL DEFAULT 0.00",
                "address": "TEXT",
                "account_type": "TEXT DEFAULT 'Savings'",
                "date_joined": "TEXT DEFAULT '2026-01-01'"
            }
            
            for col, col_def in required_columns.items():
                if col not in register_col_names:
                    try:
                        db.execute(f"ALTER TABLE register ADD COLUMN {col} {col_def}")
                    except Exception as e:
                        print(f"Could not add column {col} to register: {e}")

            # Check and add missing columns for login table
            login_columns = db.fetch_all("PRAGMA table_info(login)")
            login_col_names = {col['name'] for col in login_columns}
            
            if "epaisa_id" not in login_col_names:
                try:
                    db.execute("ALTER TABLE login ADD COLUMN epaisa_id TEXT")
                except Exception as e:
                    print(f"Could not add epaisa_id to login: {e}")

            # Check and add missing columns for transactions table
            trans_columns = db.fetch_all("PRAGMA table_info(transactions)")
            trans_col_names = {col['name'] for col in trans_columns}
            
            trans_required = {
                "sender_email": "TEXT",
                "sender_epaisa_id": "TEXT",
                "receiver_email": "TEXT", 
                "receiver_epaisa_id": "TEXT",
                "transaction_date": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "status": "TEXT DEFAULT 'completed'"
            }
            
            for col, col_def in trans_required.items():
                if col not in trans_col_names:
                    try:
                        db.execute(f"ALTER TABLE transactions ADD COLUMN {col} {col_def}")
                    except Exception as e:
                        print(f"Could not add column {col} to transactions: {e}")

            # Generate epaisa_ids for users who don't have them
            if all(c in register_col_names for c in ['username','epaisa_id','phone','email','full_name','password']):
                all_register = db.fetch_all("SELECT username, phone FROM register ORDER BY username")
                counter = 1001
                for row in all_register:
                    # Check if user already has epaisa_id
                    user_data = db.fetch_one("SELECT epaisa_id FROM register WHERE username = ?", (row['username'],))
                    if user_data and user_data.get('epaisa_id'):
                        continue
                    
                    phone = row.get("phone", "")
                    if phone and phone.startswith("98") and len(phone) >= 10:
                        new_epaisa_id = f"eP-{phone}"
                    else:
                        new_epaisa_id = f"eP-{counter}"
                        counter += 1
                    try:
                        db.execute("UPDATE register SET epaisa_id = ? WHERE username = ?", (new_epaisa_id, row["username"]))
                        db.execute("UPDATE login SET epaisa_id = ? WHERE username = ?", (new_epaisa_id, row["username"]))
                    except Exception as e:
                        print(f"Could not update epaisa_id for {row['username']}: {e}")

        except Exception as e:
            print(f"Error in table migration: {e}")

        db.close()