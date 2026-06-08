from flask import Flask
from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
    app.config["MYSQL_HOST"] = MYSQL_HOST
    app.config["MYSQL_USER"] = MYSQL_USER
    app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
    app.config["MYSQL_DATABASE"] = MYSQL_DATABASE

    from app.database import Database
    from app.routes.auth_routes import main as auth_bp
    from app.routes.user_routes import main as user_bp

    with app.app_context():
        Database.create_tables()

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app