# run.py
# Entry point for the Flask application.
# This file creates the app and starts the development server.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('Login.html')

if __name__ == '__main__':
    app.run(debug=True)