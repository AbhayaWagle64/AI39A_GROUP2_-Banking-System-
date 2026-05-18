# app/routes/profile_routes.py
# Routes for profile pages.

from flask import Blueprint
from ..controllers.profile_controller import (
    show_profile,
    show_edit_profile,
    show_settings,
    show_kyc_verification,
    show_upload_documents,
)

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

profile_bp.route('/', methods=['GET'])(show_profile)
profile_bp.route('/edit', methods=['GET'])(show_edit_profile)
profile_bp.route('/settings', methods=['GET'])(show_settings)
profile_bp.route('/kyc', methods=['GET'])(show_kyc_verification)
profile_bp.route('/upload-documents', methods=['GET'])(show_upload_documents)
