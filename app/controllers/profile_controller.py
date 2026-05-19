# app/controllers/profile_controller.py
# Controllers for profile-related pages.

from flask import render_template, request, jsonify, session
from app.models.user_model import UserModel


def show_profile():
    return render_template('profile/profile.html')


def show_edit_profile():
    return render_template('profile/edit_profile.html')


def show_settings():
    return render_template('profile/settings.html')


def show_kyc_verification():
    return render_template('profile/kyc_verification.html')


def show_upload_documents():
    return render_template('profile/upload_documents.html')



def get_user_profile_data():
    """Backend API to fetch user profile data from database."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "User session not found"}), 401

    profile_data = UserModel.get_profile_by_id(user_id)
    if profile_data:
        return jsonify({"status": "success", "data": profile_data}), 200
    else:
        return jsonify({"status": "error", "message": "Profile not found"}), 404


def update_user_profile_data():
    """Backend API to update user profile data in database."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized access"}), 401

    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')

    if not email or not phone:
        return jsonify({"status": "error", "message": "Email and Phone cannot be empty"}), 400

    is_updated = UserModel.update_profile_by_id(user_id, email, phone)
    if is_updated:
        return jsonify({"status": "success", "message": "Profile updated successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "No changes made or failed to update"}), 500