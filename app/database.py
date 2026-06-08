import pymysql
import config


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
                phone VARCHAR(20) NOT NULL UNIQUE,
                address VARCHAR(255),
                account_type VARCHAR(20) DEFAULT 'Savings',
                date_joined VARCHAR(50) DEFAULT '2026-01-01'
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS login (
                username VARCHAR(100) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL
            )
        """)
        db.close()