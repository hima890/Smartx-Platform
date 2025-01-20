"""
app_factory.py
===============

This module defines a Flask application factory, which provides a convenient way to create and configure
a Flask application using extensions such as SQLAlchemy and Flask-Migrate. The application setup includes
the integration of database configuration, database migration management, and routing for the application.

Functions:
---------
- create_app(): Factory function to create and configure the Flask application.

Dependencies:
-------------
- Flask: The core web framework used to build the web application.
- Flask-SQLAlchemy: Provides SQLAlchemy support for the Flask application, enabling database integration.
- Flask-Migrate: A tool that simplifies database migrations for SQLAlchemy.

Usage:
------
The `create_app()` function is responsible for creating and configuring the Flask application instance.
It sets the configuration using the `config.Config` class, initializes the necessary extensions (`db` and `migrate`),
registers the database with Flask, and creates all necessary database tables if they do not exist.

Database Initialization:
-------------------------
- The `db.create_all()` call within `app.app_context()` ensures that all tables in the database are created 
  if they do not already exist. This setup supports database version control and migrations.

Blueprint Integration:
------------------------
- The application is set up to use the blueprint system in Flask, with routes registered from the `main` blueprint 
  located in the `.routes` module.

Returns:
--------
- Returns the configured Flask application instance.

Example:
--------
```python
app = create_app()
app.run(debug=True)

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Create all tables in the database (if they do not exist)
    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app
