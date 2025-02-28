from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('Assessment', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)  # technical, creative, interpersonal
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Store answers as JSON
    answers = db.Column(db.JSON)

class CareerPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.JSON)  # Store as JSON array
    salary_range = db.Column(db.String(50))
    growth_potential = db.Column(db.Float)  # Score from 0-1
    match_score = db.Column(db.Float)  # Score from 0-1
