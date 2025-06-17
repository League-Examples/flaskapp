"""
Setup script for flaskapp package.
"""
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="flaskapp",
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            "flask.commands": [
                "cmd1=flaskapp.cli.cmd1:cmd1_command",
                "cmd2=flaskapp.cli.cmd2:cmd2_command",
                "config=flaskapp.cli.config:config_command",
                "dev=flaskapp.cli.dev:dev_cli",
            ],
        },
    )