from flask import Blueprint, jsonify

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    """Login route."""
    return jsonify({"message": "Login endpoint"})

@auth_bp.route('/register')
def register():
    """Registration route."""
    return jsonify({"message": "Registration endpoint"})