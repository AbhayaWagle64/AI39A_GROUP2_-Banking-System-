# app/database.py
# Database helper functions. Use this file to create the database tables.

from .extensions import db


def init_database(app):
    with app.app_context():
        db.create_all()
        print('Database has been initialized.')
