# run.py
# Entry point for the Flask application.
# This file creates the app and starts the development server.

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
