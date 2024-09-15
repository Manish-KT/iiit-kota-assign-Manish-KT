from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    """
    Create and configure an instance of the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
    CORS(app)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb.db'
    db.init_app(app)

    # Image upload folder configuration
    UPLOAD_FOLDER = 'images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Import routes and register them
    from routes import register_routes
    register_routes(app, db)
    
    # Set up database migrations
    Migrate(app, db)
    
    return app
