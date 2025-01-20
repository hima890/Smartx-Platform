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
