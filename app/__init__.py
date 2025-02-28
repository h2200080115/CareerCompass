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
    migrate = Migrate(app, db)  # Add Flask-Migrate

    with app.app_context():
        # Import models
        from .models import User, Assessment, CareerPath

        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Add sample career paths
        sample_careers = [
            {
                'title': 'Software Developer',
                'description': 'Design and develop software applications using various programming languages and frameworks.',
                'required_skills': ['Python', 'JavaScript', 'SQL', 'Problem Solving'],
                'salary_range': '$70,000 - $150,000',
                'growth_potential': 0.85,
                'match_score': 0.9,
                'education_requirements': "Bachelor's degree in Computer Science or related field",
                'experience_level': 'Entry to Mid-Level',
                'industry': 'Technology',
                'job_outlook': 'Excellent growth prospects with increasing demand for software developers',
                'certification_requirements': ['AWS Certified Developer', 'Microsoft Certified: Azure Developer']
            },
            {
                'title': 'UX Designer',
                'description': 'Create user-friendly interfaces and optimize user experiences for websites and applications.',
                'required_skills': ['UI Design', 'User Research', 'Prototyping', 'Wireframing'],
                'salary_range': '$60,000 - $120,000',
                'growth_potential': 0.8,
                'match_score': 0.85,
                'education_requirements': "Bachelor's degree in Design or related field",
                'experience_level': 'Entry to Mid-Level',
                'industry': 'Technology/Design',
                'job_outlook': 'Strong demand for UX designers across industries',
                'certification_requirements': ['Google UX Design Certificate']
            },
            {
                'title': 'Data Scientist',
                'description': 'Analyze complex data sets to help guide business decisions.',
                'required_skills': ['Python', 'R', 'Machine Learning', 'Statistics'],
                'salary_range': '$75,000 - $160,000',
                'growth_potential': 0.9,
                'match_score': 0.8,
                'education_requirements': "Master's degree in Data Science, Statistics, or related field",
                'experience_level': 'Mid-Level',
                'industry': 'Technology/Analytics',
                'job_outlook': 'High demand with growing emphasis on data-driven decision making',
                'certification_requirements': ['AWS Certified Machine Learning', 'IBM Data Science Professional Certificate']
            }
        ]

        for career_data in sample_careers:
            career = CareerPath(**career_data)
            db.session.add(career)

        db.session.commit()

        # Register blueprints
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .chat import chat as chat_blueprint
        app.register_blueprint(chat_blueprint)

        return app