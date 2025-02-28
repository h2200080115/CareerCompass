from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Assessment, CareerPath
import json

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/assessment')
@login_required
def assessment():
    return render_template('assessment/index.html')

@main.route('/assessment/<type>')
@login_required
def take_assessment(type):
    if type not in ['technical', 'creative', 'interpersonal']:
        return redirect(url_for('main.assessment'))
    
    # Check if assessment already taken
    existing = Assessment.query.filter_by(
        user_id=current_user.id,
        assessment_type=type,
        completed=True
    ).first()
    
    if existing:
        flash('You have already completed this assessment.')
        return redirect(url_for('main.assessment'))
        
    template = f'assessment/{type}.html'
    return render_template(template)

@main.route('/assessment/submit', methods=['POST'])
@login_required
def submit_assessment():
    data = request.get_json()
    
    assessment = Assessment(
        user_id=current_user.id,
        assessment_type=data['type'],
        answers=data['answers'],
        score=data['score'],
        completed=True
    )
    
    db.session.add(assessment)
    db.session.commit()
    
    return jsonify({'status': 'success'})

@main.route('/recommendations')
@login_required
def recommendations():
    # Get completed assessments
    assessments = Assessment.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).all()
    
    # Get career recommendations based on assessment scores
    careers = CareerPath.query.all()
    
    return render_template('recommendations.html', 
                         assessments=assessments,
                         careers=careers)

@main.route('/resources')
@login_required
def resources():
    return render_template('resources.html')
