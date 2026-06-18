# Kalyan - Database Setup
# Sprint 1 - Story #1: User Registration (Baibhav frontend + Sakina backend)
# Sprint 2 - Story #10: Receive Money (Nischal frontend + Sakina backend)

import mysql.connector

def create_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin#abhaya64$'
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS epaisa")
    cursor.execute("USE epaisa")

    # Story #1 - User Registration (Baibhav's form fields)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL,
            dob DATE,
            password VARCHAR(255) NOT NULL,
            pan VARCHAR(50),
            referral VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Story #1 - Wallet created on registration (Sakina's model)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            balance FLOAT DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Story #10 - Receive Money transactions (Nischal's wallet display)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT NOT NULL,
            receiver_id INT NOT NULL,
            amount FLOAT NOT NULL,
            title VARCHAR(255),
            type VARCHAR(50),
            status VARCHAR(50) DEFAULT 'completed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    """)

    # Story #10 - Linked accounts (Nischal's linked accounts display)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS linked_accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            account_number VARCHAR(50) NOT NULL,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)


    # Story #12 - OTP Verification (Kalyan backend)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otp_verifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            otp VARCHAR(6) NOT NULL,
            amount FLOAT NOT NULL,
            receiver_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_used TINYINT(1) DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete!")

if __name__ == '__main__':
    create_database()

    