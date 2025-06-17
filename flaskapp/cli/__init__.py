"""
CLI commands for the Flask application.
"""

from flaskapp.cli.config import config_command
from flaskapp.cli.dev import dev_cli

__all__ = ['cmd1_command', 'cmd2_command', 'config_command', 'dev_cli']