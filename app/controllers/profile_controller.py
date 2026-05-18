# app/controllers/profile_controller.py
# Controllers for profile-related pages.

from flask import render_template


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
