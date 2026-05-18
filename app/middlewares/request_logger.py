# app/middlewares/request_logger.py
# Middleware that logs every request.

from flask import request


def init_request_logger(app):
    @app.before_request
    def log_request():
        print(f'Request: {request.method} {request.path}')
