import os

SECRET_KEY = "epaisa-secret-key-2026"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "admin#abhaya64$"
MYSQL_DATABASE = "ePaisa"

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "app", "static", "uploads"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}