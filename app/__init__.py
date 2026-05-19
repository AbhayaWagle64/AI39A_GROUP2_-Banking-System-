import os
from flask import Flask
from app.extensions import db
from app.database import init_database

# 1. Profile controller backend imports
from app.controllers.profile_controller import (
    get_user_profile_data, 
    update_user_profile_data
)

def create_app():
    # Initialize the Flask application instance
    app = Flask(__name__)
    
    # Load configuration settings from your root config.py file
    app.config.from_object('config.Config')
    
    # Initialize your team's database configuration with this app context
    db.init_app(app)
    init_database(app)
    
    # 2. Your API Routes for User Story 4 (Profile Management)
    @app.route('/api/profile', methods=['GET'])
    def api_get_profile():
        """URL path that the frontend fetches to get profile info"""
        response, status_code = get_user_profile_data()
        return response, status_code

    @app.route('/api/profile/update', methods=['POST'])
    def api_update_profile():
        """URL path that the frontend posts to when hitting 'Save'"""
        response, status_code = update_user_profile_data()
        return response, status_code

    # Return the fully configured app instance to run.py
    return app