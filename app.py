import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy with custom base
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    logger.info("Creating Flask application...")
    app = Flask(__name__)

    # Configure app
    app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///images.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

    try:
        # Initialize extensions
        logger.info("Initializing database...")
        db.init_app(app)

        logger.info("Initializing login manager...")
        login_manager.init_app(app)
        login_manager.login_view = 'login'

        # Add health check route
        @app.route('/health')
        def health_check():
            return 'OK', 200

        logger.info("Application initialization complete!")
        return app
    except Exception as e:
        logger.error(f"Error during application initialization: {str(e)}")
        raise

# Create the application instance
app = create_app()

# Import routes and models after app instance is created
import routes  # noqa: F401
import models  # noqa: F401

# Create database tables
with app.app_context():
    # Delete the old database file if it exists
    db_path = os.path.join(os.path.dirname(app.instance_path), 'instance', 'images.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info("Removed old database file")

    # Create all tables
    db.create_all()
    logger.info("Created new database tables")