from flask import Blueprint, render_template, jsonify

# Create a Blueprint for the main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page route."""
    return jsonify({"message": "Welcome to FlaskApp API!"})

@main_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})