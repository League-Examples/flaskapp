"""
Flask application factory module.
This module contains the application factory function that creates and configures
the Flask application instance.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """
    Application factory function.
    Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__)
    
    # Determine the configuration to use
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Load the appropriate configuration
    if config_name == 'production':
        app.config.from_object('flaskapp.config.production.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('flaskapp.config.testing.TestingConfig')
    else:
        app.config.from_object('flaskapp.config.development.DevelopmentConfig')
    
    # Initialize extensions with the app
    db.init_app(app)
    
    # Register blueprints
    from flaskapp.main.routes import main_bp
    app.register_blueprint(main_bp)
    
    from flaskapp.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register CLI commands
    from flaskapp.cli import cmd1_command, cmd2_command
    app.cli.add_command(cmd1_command)
    app.cli.add_command(cmd2_command)
    
    return app