from flask import Flask
from app.session_manager import configure_session


def create_app():

    app = Flask(
        __name__,
        template_folder="templets",
        static_folder="templets/static"
    )

    # SECRET KEY (sessions)
    app.secret_key = "epaisa_secret_key_123"

    # Session timeout setup
    configure_session(app)

    # Import routes
    from app.routes import init_routes
    init_routes(app)

    return app