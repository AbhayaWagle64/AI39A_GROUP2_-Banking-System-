# databse 
import config
import pymysql


class Database:
    def __init__(self):
        self.__connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def fetch_one(self, query, params=None):
        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None):
        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def execute(self, query, params=None):
        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        self.__connection.commit()
        cursor.close()

    def close(self):
        self.__connection.close()

    @staticmethod
    def create_tables():
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS administration (
                id INT AUTO_INCREMENT PRIMARY KEY,
                admin_email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS register (
                username VARCHAR(100) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone VARCHAR(20) NOT NULL,
                customer_id VARCHAR(20) UNIQUE,
                epaisa_id VARCHAR(20) UNIQUE NOT NULL,
                balance DECIMAL(10,2) DEFAULT 0.00,
                address VARCHAR(255),
                account_type VARCHAR(20) DEFAULT 'Savings',
                date_joined VARCHAR(50) DEFAULT '2026-01-01'
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS login (
                username VARCHAR(100) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                epaisa_id VARCHAR(20)
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_email VARCHAR(100),
                sender_epaisa_id VARCHAR(20),
                receiver_email VARCHAR(100),
                receiver_epaisa_id VARCHAR(20),
                amount DECIMAL(10,2),
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'completed'
            )
        """)

        # Insert default admin users
        from werkzeug.security import generate_password_hash
        for admin_email, admin_password in [('admin@admin.com', 'Admin#AW64'), ('admin1@admin.com', 'Admin1#AW64')]:
            existing = db.fetch_one("SELECT * FROM administration WHERE admin_email = %s", (admin_email,))
            if not existing:
                db.execute(
                    "INSERT INTO administration (admin_email, password) VALUES (%s, %s)",
                    (admin_email, generate_password_hash(admin_password))
                )

        def add_column_if_missing(table, col, col_def):
            cols = db.fetch_all(f"SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name='{table}' AND table_schema=DATABASE()")
            names = {r.get('COLUMN_NAME','') for r in cols}
            if col not in names:
                try:
                    db.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
                except Exception:
                    pass

        add_column_if_missing("register", "epaisa_id", "epaisa_id VARCHAR(20)")
        add_column_if_missing("register", "customer_id", "customer_id VARCHAR(20) UNIQUE")
        add_column_if_missing("register", "balance", "balance DECIMAL(10,2) DEFAULT 0.00")
        add_column_if_missing("register", "address", "address VARCHAR(255)")
        add_column_if_missing("register", "account_type", "account_type VARCHAR(20) DEFAULT 'Savings'")
        add_column_if_missing("register", "date_joined", "date_joined VARCHAR(50) DEFAULT '2026-01-01'")
        add_column_if_missing("login", "epaisa_id", "epaisa_id VARCHAR(20)")
        add_column_if_missing("transactions", "sender_email", "sender_email VARCHAR(100)")
        add_column_if_missing("transactions", "sender_epaisa_id", "sender_epaisa_id VARCHAR(20)")
        add_column_if_missing("transactions", "receiver_email", "receiver_email VARCHAR(100)")
        add_column_if_missing("transactions", "receiver_epaisa_id", "receiver_epaisa_id VARCHAR(20)")
        add_column_if_missing("transactions", "transaction_date", "transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        add_column_if_missing("transactions", "status", "status VARCHAR(20) DEFAULT 'completed'")

        cols_check = db.fetch_all("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name='register' AND table_schema=DATABASE()")
        col_names = {r.get('COLUMN_NAME','') for r in cols_check}
        if all(c in col_names for c in ('username','epaisa_id','phone','email','full_name','password','address','account_type','date_joined')):
            already_new = db.fetch_one("SELECT COUNT(*) AS cnt FROM register WHERE epaisa_id REGEXP %s", ("^eP-(98[0-9]{8}|100[0-9]+)$",))
            cnt = already_new.get("cnt", 0) if already_new else 0
            if cnt == 0:
                all_register = db.fetch_all("SELECT username, phone FROM register ORDER BY username")
                counter = 1001
                for row in all_register:
                    phone = row.get("phone", "")
                    if phone and phone.startswith("98") and len(phone) >= 10:
                        new_epaisa_id = f"eP-{phone}"
                    else:
                        new_epaisa_id = f"eP-{counter}"
                        counter += 1
                    db.execute("UPDATE register SET epaisa_id = %s WHERE username = %s", (new_epaisa_id, row["username"]))
                    db.execute("UPDATE login SET epaisa_id = %s WHERE username = %s", (new_epaisa_id, row["username"]))

        t_cols = db.fetch_all("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name='transactions' AND table_schema=DATABASE()")
        t_col_names = {r.get('COLUMN_NAME','') for r in t_cols}
        old_cols = ["sender_username", "recipient_username", "recipient_name", "created_at"]
        for col in old_cols:
            if col in t_col_names:
                try:
                    db.execute(f"ALTER TABLE transactions DROP COLUMN {col}")
                except Exception:
                    try:
                        fk_row = db.fetch_one(
                            "SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='transactions' AND COLUMN_NAME=%s AND REFERENCED_TABLE_NAME IS NOT NULL",
                            (col,)
                        )
                        if fk_row and fk_row.get('CONSTRAINT_NAME'):
                            db.execute(f"ALTER TABLE transactions DROP FOREIGN KEY {fk_row['CONSTRAINT_NAME']}")
                            db.execute(f"ALTER TABLE transactions DROP COLUMN {col}")
                    except Exception:
                        pass

        db.close()