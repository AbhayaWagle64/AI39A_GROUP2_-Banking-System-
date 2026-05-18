# app/errors/handlers.py
# Register friendly error pages and handlers.

from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(403)
    def handle_403(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def handle_404(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def handle_500(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        return render_template('errors/maintenance.html', message=str(error)), 500
