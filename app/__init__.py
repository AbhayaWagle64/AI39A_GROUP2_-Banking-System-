# app/__init__.py
# Application factory for Flask. This file creates and configures the Flask app.

from flask import Flask
from .extensions import db
from .routes import register_blueprints
from .errors.handlers import register_error_handlers
from .middlewares.rate_limiter import init_rate_limiter
from .middlewares.request_logger import init_request_logger


def create_app(config_class=None):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class or 'config.Config')
    db.init_app(app)
    register_blueprints(app)
    register_error_handlers(app)
    init_rate_limiter(app)
    init_request_logger(app)
    return app
