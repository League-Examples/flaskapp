"""
WSGI entry point for the Flask application.
This module defines the app instance that will be used by the WSGI server (Gunicorn).
"""
from flaskapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run()