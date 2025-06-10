"""
Flask application factory module.
This module contains the application factory function that creates and configures
the Flask application instance.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_font_awesome import FontAwesome
from flask_login import current_user

# Initialize extensions
db = SQLAlchemy()
bootstrap = Bootstrap5()
fa = FontAwesome()

def create_app():
    """
    Application factory function.
    Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__,
                template_folder='templates')  # Explicitly define the template folder
    
    # Determine the configuration to use
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Load the appropriate configuration
    if config_name == 'production':
        app.config.from_object('flaskapp.config.production.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('flaskapp.config.testing.TestingConfig')
    else:
        app.config.from_object('flaskapp.config.development.DevelopmentConfig')
    

    # Allow OAuth over http in debug mode for development
    if app.debug or os.environ.get('FLASK_ENV') == 'development':
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Initialize extensions with the app
    db.init_app(app)
    bootstrap.init_app(app)
    fa.init_app(app)
    
    # Register blueprints
    from flaskapp.main.routes import main_bp
    app.register_blueprint(main_bp)
    

    from flaskapp.demo import demo_bp
    app.register_blueprint(demo_bp)

    import  flaskapp.auth 
    flaskapp.auth.init_app(app)
    

    # Create database tables
    with app.app_context():
        db.create_all()
    

    @app.context_processor
    def inject_common_variables():
        """
        Inject common variables into the template context.
        """
        from importlib.metadata import metadata, version

        meta = metadata("flaskapp")
        

        return {
            "current_user": current_user,
            'meta': {
                "site_name": meta["Name"],
                "version": version(meta["Name"]), 
            }
        }
    

    return app