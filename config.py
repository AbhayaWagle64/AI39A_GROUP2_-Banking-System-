import os


SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "1234")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "epaisa_db")


class Config:
    SECRET_KEY = SECRET_KEY
    MYSQL_HOST = MYSQL_HOST
    MYSQL_USER = MYSQL_USER
    MYSQL_PASSWORD = MYSQL_PASSWORD
    MYSQL_DATABASE = MYSQL_DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///instance/epaisa.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
