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
        db.execute("""
            CREATE TABLE IF NOT EXISTS recharges (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL,
                transaction_id INT NULL,
                mobile_number VARCHAR(15) NOT NULL,
                operator VARCHAR(50) NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                plan_description VARCHAR(255),
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (transaction_id)
                REFERENCES transactions(id)
                ON DELETE SET NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS saved_payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL,
                recipient_name VARCHAR(100) NOT NULL,
                recipient_email VARCHAR(150),
                recipient_phone VARCHAR(20),
                nickname VARCHAR(50),
                payment_type VARCHAR(30) DEFAULT 'wallet_transfer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                transaction_type VARCHAR(30),
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'completed'
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS wrong_transaction_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                transaction_id INT NOT NULL,
                reason VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS profile_management (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                address VARCHAR(255),
                account_type VARCHAR(20) DEFAULT 'Savings',
                profile_picture VARCHAR(255),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
           )
        """)

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
        add_column_if_missing("recharges","user_id","user_id VARCHAR(100) NOT NULL")
        add_column_if_missing("recharges","transaction_id","transaction_id INT NULL")
        add_column_if_missing("recharges","mobile_number","mobile_number VARCHAR(15) NOT NULL")
        add_column_if_missing("recharges","operator","operator VARCHAR(50) NOT NULL")
        add_column_if_missing("recharges","amount","amount DECIMAL(10,2) NOT NULL")
        add_column_if_missing("recharges","plan_description","plan_description VARCHAR(255)")
        add_column_if_missing("recharges","status","status VARCHAR(20) DEFAULT 'pending'")
        add_column_if_missing("recharges","created_at","created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        add_column_if_missing("saved_payments","user_id","user_id VARCHAR(100) NOT NULL")
        add_column_if_missing("saved_payments","recipient_name","recipient_name VARCHAR(100) NOT NULL")
        add_column_if_missing("saved_payments","recipient_email","recipient_email VARCHAR(150)")
        add_column_if_missing("saved_payments","recipient_phone","recipient_phone VARCHAR(20)")
        add_column_if_missing("saved_payments","nickname","nickname VARCHAR(50)")
        add_column_if_missing("saved_payments","payment_type","payment_type VARCHAR(30) DEFAULT 'wallet_transfer'")
        add_column_if_missing("saved_payments","created_at","created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        add_column_if_missing("transactions","transaction_type","transaction_type VARCHAR(30)")
        add_column_if_missing("register","balance","balance DECIMAL(10,2) DEFAULT 0.00")
        add_column_if_missing("wrong_transaction_reports","username","username VARCHAR(100) NOT NULL")
        add_column_if_missing("wrong_transaction_reports","transaction_id","transaction_id INT NOT NULL")
        add_column_if_missing("wrong_transaction_reports","reason","reason VARCHAR(255) NOT NULL")
        add_column_if_missing("wrong_transaction_reports","description","description TEXT")
        add_column_if_missing("wrong_transaction_reports","status","status VARCHAR(20) DEFAULT 'pending'")
        add_column_if_missing("wrong_transaction_reports","created_at","created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        add_column_if_missing("profile_management","username","username VARCHAR(100) NOT NULL")
        add_column_if_missing("profile_management","full_name","full_name VARCHAR(100) NOT NULL")
        add_column_if_missing("profile_management","email","email VARCHAR(100) NOT NULL")
        add_column_if_missing("profile_management","phone","phone VARCHAR(20)")
        add_column_if_missing("profile_management","address","address VARCHAR(255)")
        add_column_if_missing("profile_management","account_type","account_type VARCHAR(20) DEFAULT 'Savings'")
        add_column_if_missing("profile_management","profile_picture","profile_picture VARCHAR(255)")
        add_column_if_missing("profile_management","updated_at","updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

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