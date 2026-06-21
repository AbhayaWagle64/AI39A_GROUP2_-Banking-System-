from datetime import timedelta


SESSION_TIMEOUT = timedelta(minutes=10)


def configure_session(app):

    app.permanent_session_lifetime = SESSION_TIMEOUT