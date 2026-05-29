# run.py
# Entry point for the Flask application.
# This file creates the app and starts the development server.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('Login.html')
@app.route('/')
def register():
    return render_template('register.html')
@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True)