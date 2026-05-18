# app/routes/bills_routes.py
# Routes for bill payment pages.

from flask import Blueprint
from ..controllers.bills_controller import (
    show_bill_history,
    show_electricity_bill,
    show_internet_bill,
    show_mobile_recharge,
    show_tv_bill,
    show_water_bill,
)

bills_bp = Blueprint('bills', __name__, url_prefix='/bills')

bills_bp.route('/', methods=['GET'])(show_bill_history)
bills_bp.route('/electricity', methods=['GET'])(show_electricity_bill)
bills_bp.route('/internet', methods=['GET'])(show_internet_bill)
bills_bp.route('/mobile', methods=['GET'])(show_mobile_recharge)
bills_bp.route('/tv', methods=['GET'])(show_tv_bill)
bills_bp.route('/water', methods=['GET'])(show_water_bill)
