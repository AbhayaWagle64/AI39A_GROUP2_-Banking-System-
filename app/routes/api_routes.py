# app/routes/api_routes.py
# Example API blueprint for JSON responses.

from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status', methods=['GET'])
def api_status():
    return jsonify({'status': 'ok', 'message': 'ePaisa API is live'})
