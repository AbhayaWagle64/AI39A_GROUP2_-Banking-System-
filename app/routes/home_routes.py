# app/routes/home_routes.py
# Root route for the web application.

from flask import Blueprint
from ..controllers.home_controller import show_home

home_bp = Blueprint('home', __name__)

home_bp.route('/', methods=['GET'])(show_home)
