import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    # Use SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_advisor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        # Import models
        from .models import User, Assessment, CareerPath

        # Create tables
        db.create_all()

        # Register blueprints
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .chat import chat as chat_blueprint
        app.register_blueprint(chat_blueprint)

        return app