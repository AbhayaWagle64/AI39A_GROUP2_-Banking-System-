from flask import Flask
<<<<<<< HEAD
from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
=======
from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
>>>>>>> abhaya-wagle


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
<<<<<<< HEAD
=======
    app.config["MYSQL_HOST"] = MYSQL_HOST
    app.config["MYSQL_USER"] = MYSQL_USER
    app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
    app.config["MYSQL_DATABASE"] = MYSQL_DATABASE
>>>>>>> abhaya-wagle
    app.config["MAIL_SERVER"] = MAIL_SERVER
    app.config["MAIL_PORT"] = MAIL_PORT
    app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
    app.config["MAIL_USERNAME"] = MAIL_USERNAME
    app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
    app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER

    from app.database import Database
    from app.routes.auth_routes import main as auth_bp
    from app.routes.user_routes import main as user_bp
    from app.routes.admin_routes import main as admin_bp
    from app.utils.mailer import Mailer

    with app.app_context():
        Database.create_tables()

    mailer = Mailer(app)
    app.mailer = mailer

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
<<<<<<< HEAD
=======

    @app.before_request
    def _check_one_week_cookie():
        from flask import request, session
        token = request.cookies.get('one_week_token')
        if not token:
            return
        # if session already has user, nothing to do
        if session.get('user_id'):
            return
        try:
            from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
            from app.models.login_model import LoginModel
            s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            data = s.loads(token, max_age=7*24*3600)
            username = data.get('username')
            if username:
                # ensure login record still exists and set session to auto-login
                lm = LoginModel()
                record = lm.find_by_username(username)
                if record:
                    session['user_id'] = username
        except Exception:
            # expired or invalid token: attempt to remove any stale login record
            try:
                from itsdangerous import URLSafeTimedSerializer
                from app.models.login_model import LoginModel
                s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
                data = s.loads(token)
                username = data.get('username')
                if username:
                    LoginModel().delete(username)
            except Exception:
                pass
>>>>>>> abhaya-wagle

    return app