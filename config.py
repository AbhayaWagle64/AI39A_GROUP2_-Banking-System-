import os


def _load_dotenv():
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    values = {}
    if not os.path.exists(dotenv_path):
        return values

    with open(dotenv_path, "r", encoding="utf-8") as dotenv_file:
        for line in dotenv_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


ENV_VALUES = _load_dotenv()


def _get_env(name, default=""):
    return os.environ.get(name, ENV_VALUES.get(name, default))


SECRET_KEY = _get_env("SECRET_KEY", "epaisa-secret-key-2026")
MYSQL_HOST = _get_env("MYSQL_HOST", "localhost")
MYSQL_USER = _get_env("MYSQL_USER", "root")
MYSQL_PASSWORD = _get_env("MYSQL_PASSWORD", "lakpa123$$$$@.>!")
MYSQL_DATABASE = _get_env("MYSQL_DATABASE", "epaisa")

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "app", "static", "uploads"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

MAIL_SERVER = _get_env("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(_get_env("MAIL_PORT", 587))
MAIL_USE_TLS = _get_env("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
MAIL_USERNAME = _get_env("MAIL_USERNAME", "")
MAIL_PASSWORD = _get_env("MAIL_PASSWORD", "")
MAIL_DEFAULT_SENDER = _get_env("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
