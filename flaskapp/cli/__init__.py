"""
CLI commands for the Flask application.
"""
from flaskapp.cli.cmd1 import cmd1_command
from flaskapp.cli.cmd2 import cmd2_command
from flaskapp.cli.dev import dev_cli

__all__ = ['cmd1_command', 'cmd2_command', 'dev_cli']