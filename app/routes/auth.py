from flask import Blueprint, render_template, request, redirect, url_for, flash

class AuthRoutes:
    def register(self):
        auth_bp = Blueprint('auth', __name__)

        @auth_bp.route('/', methods=['GET', 'POST'])
        def home():
            return render_template('login.html')

        @auth_bp.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')
                
                print(f"Login attempt by: {email}") # Visible in your VS Code terminal
                
                # For testing right now, let's redirect straight to the dashboard:
                return redirect('/dashboard')

            return render_template('login.html')

        @auth_bp.route('/register', methods=['GET', 'POST'])
        def register_user():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                
                print(f"New user submitting form: {username} - {email}") # Visible in your terminal
                
                return redirect('/login') 
            
            return render_template('auth/register.html')

        return auth_bp