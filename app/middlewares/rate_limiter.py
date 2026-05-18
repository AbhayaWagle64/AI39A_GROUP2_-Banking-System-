# app/middlewares/rate_limiter.py
# Basic rate limiter placeholder.

from flask import request


def init_rate_limiter(app):
    @app.before_request
    def simple_rate_limit():
        # This is only a demo; a real app should use Redis or another store.
        if request.path.startswith('/api'):
            pass
