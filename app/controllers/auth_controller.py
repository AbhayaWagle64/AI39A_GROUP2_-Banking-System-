import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for, session, render_template, request
from app.controllers.base_controller import BaseController
from app.database import Database
from app.models.register_model import RegisterModel
from app.models.login_model import LoginModel


class AuthController(BaseController):
    def __init__(self, app=None):
        if app:
            super().__init__(app)
        self.register_model = RegisterModel()
        self.login_model = LoginModel()
        self.customer_id_counter = 10001

    def validate_phone(self, phone):
        return bool(re.fullmatch(r'98\d{8}', phone))

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def get_current_user(self):
        user_id = session.get("user_id")
        if not user_id:
            return None
        login_data = self.login_model.find_by_username(user_id)
        if not login_data:
            return None
        register_data = self.register_model.find_by_username(user_id)
        return {
            "username": user_id,
            "full_name": login_data.get("full_name", user_id),
            "customer_id": f"SB-{self.customer_id_counter}",
            "email": register_data.get("email", "") if register_data else "",
            "phone": register_data.get("phone", "") if register_data else "",
            "address": register_data.get("address", "") if register_data else "",
            "account_type": register_data.get("account_type", "Savings") if register_data else "Savings",
            "date_joined": register_data.get("date_joined", "") if register_data else "",
            "balance": "12,450.00"
        }

    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                flash('Username/email and password are required.', 'danger')
                return render_template("login.html")

            login_data = self.login_model.find_by_username(username)
            if login_data:
                if check_password_hash(login_data['password'], password):
                    session['user_id'] = username
                    flash('Login successful!', 'success')
                    return redirect(url_for('user.wallet'))
                else:
                    flash('Wrong username or password.', 'danger')
                    return render_template("login.html")
            
            reg_data = self.register_model.find_by_username(username)
            if not reg_data:
                db = Database()
                results = db.fetch_all("SELECT * FROM register WHERE email = %s", (username,))
                db.close()
                if results:
                    reg_data = results[0]
            
            if reg_data:
                if check_password_hash(reg_data['password'], password):
                    self.login_model.create(reg_data['username'], reg_data['password'], reg_data['full_name'])
                    session['user_id'] = reg_data['username']
                    flash('Login successful!', 'success')
                    return redirect(url_for('user.wallet'))
                else:
                    flash('Wrong username or password.', 'danger')
                    return render_template("login.html")
            else:
                flash('Wrong username or password.', 'danger')
                return render_template("login.html")

        return render_template("login.html")

    def _get_all_registered(self):
        db = Database()
        results = db.fetch_all("SELECT * FROM register")
        db.close()
        return {(r['username']): r for r in results}.items()

    def register(self):
        if request.method == 'POST':
            full_name = request.form.get('fullname', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')

            if not email or not password:
                flash('Email and password are required.', 'danger')
                return render_template("register.html")

            if not full_name:
                flash('Full name is required.', 'danger')
                return render_template("register.html")

            if not self.validate_phone(phone):
                flash('Phone number must be exactly 10 digits starting with 98 (e.g. 9812345678).', 'danger')
                return render_template("register.html")

            if '@' not in email:
                flash('Please enter a valid email address.', 'danger')
                return render_template("register.html")

            if not self.validate_password(password):
                flash('Password must be at least 8 characters with 1 uppercase letter, 1 number, and 1 special character.', 'danger')
                return render_template("register.html")

            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template("register.html")

            username = email

            if self.register_model.find_by_email(email):
                flash("An account with this email already exists.", 'danger')
                return render_template("register.html")

            if self.register_model.find_by_username(username):
                flash("An account with this username already exists.", 'danger')
                return render_template("register.html")

            self.register_model.create(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone,
                address='',
                account_type='Savings',
                date_joined='2026-01-01'
            )

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))

        return render_template("register.html")

    def logout(self):
        user_id = session.get("user_id")
        if user_id:
            self.login_model.delete(user_id)
        session.clear()
        flash("Logged out successfully.", "success")
        return redirect(url_for("auth.login"))
