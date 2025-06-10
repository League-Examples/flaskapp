"""
Setup script for flaskapp package.
"""
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="flaskapp",
        packages=find_packages(),
        include_package_data=True,
    )