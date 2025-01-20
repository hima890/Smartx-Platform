"""
Module: config.py
==================

This module is responsible for loading and managing the application's configuration settings. 
It utilizes environment variables to define essential settings, ensuring flexibility and security 
by decoupling configuration details from the codebase.

Classes:
--------
- Config: A configuration class containing settings for the application, including the secret key, 
          database URI, and debug mode.

Functions:
----------
None

External Libraries:
--------------------
- os: Provides a way to interact with the operating system, specifically for accessing environment variables.
- dotenv.load_dotenv: Loads environment variables from a .env file into the application's environment.

Environment Variables:
-----------------------
The following variables should be defined in the `.env` file or system environment:
- SECRET_KEY: A secret key used for application security, such as session management.
- DEBUG: A flag to enable or disable debug mode.
- SQLALCHEMY_DATABASE_URI: The URI for the database connection.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file in the current directory.
load_dotenv("./.env")

class Config:
    """
    A configuration class that holds the application's settings.

    Attributes:
    -----------
    SECRET_KEY (str): 
        The secret key for the application, used for cryptographic operations. 
        Default is 'default_secret_key' if not provided in the environment.

    DEBUG (str or None): 
        The debug mode of the application. When set to 'True', debug mode is enabled.

    SQLALCHEMY_TRACK_MODIFICATIONS (bool): 
        Determines whether to track modifications of objects and emit signals. 
        Defaults to `False` for performance optimization.

    SQLALCHEMY_DATABASE_URI (str or None): 
        The database URI for the application. Used by SQLAlchemy to connect to the database.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
