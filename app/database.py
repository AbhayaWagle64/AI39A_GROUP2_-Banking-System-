import sqlite3

DATABASE_NAME = "epaisa.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet_id TEXT UNIQUE,
        name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password TEXT NOT NULL,
        failed_attempts INTEGER DEFAULT 0,
        account_locked INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet_id TEXT UNIQUE,
        user_id INTEGER,
        balance REAL DEFAULT 0,
        status TEXT DEFAULT 'ACTIVE',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
     # TRANSACTIONS TABLE  👈 ADD HERE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_wallet TEXT,
        receiver_wallet TEXT,
        amount REAL,
        fee REAL,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # OTP TABLE  👈 ADD HERE
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp_verifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id INTEGER,
        otp_code TEXT,
        expires_at TIMESTAMP,
        verified INTEGER DEFAULT 0
    )
    """)

    # NOTIFICATIONS TABLE 👈 ADD HERE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet_id TEXT,
        title TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()