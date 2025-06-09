"""
Demo blueprint for the Flask application.
This module contains the demo blueprint with sample pages.
"""
from flask import Blueprint

demo_bp = Blueprint('demo', __name__, url_prefix='/demo', 
                    template_folder='templates', static_folder='static')

from flaskapp.demo import routes
