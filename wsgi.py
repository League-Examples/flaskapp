"""
WSGI entry point for the Flask application.
This module defines the app instance that will be used by the WSGI server (Gunicorn).
"""
from flaskapp import FlaskApp

app = FlaskApp()

if __name__ == "__main__":
    app.run()