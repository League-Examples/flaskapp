from flask import Blueprint, render_template, jsonify, current_app
from flask_login import current_user

# Create a Blueprint for the main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page route."""
    return render_template('main/index.html', user=current_user)

@main_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})