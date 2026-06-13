# run.py
# Entry point for the Flask application.
# This file creates the app and starts the development server.

from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/sendmoney')
def sendmoney():
    return render_template('send_money.html')

if __name__ == '__main__':
    app.run(debug=True)