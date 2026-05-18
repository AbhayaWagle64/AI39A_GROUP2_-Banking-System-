# app/routes/qr_routes.py
# Routes for QR-related pages.

from flask import Blueprint
from ..controllers.qr_controller import (
    show_qr_payment,
    show_generate_qr,
    show_scan_qr,
)

qr_bp = Blueprint('qr', __name__, url_prefix='/qr')

qr_bp.route('/', methods=['GET'])(show_qr_payment)
qr_bp.route('/generate', methods=['GET'])(show_generate_qr)
qr_bp.route('/scan', methods=['GET'])(show_scan_qr)
