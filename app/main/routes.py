from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Assessment, CareerPath, JobApplication
import json
import logging

logger = logging.getLogger(__name__)

@main.route('/profile')
@login_required
def profile():
    try:
        # Get user's completed assessments
        assessments = Assessment.query.filter_by(
            user_id=current_user.id
        ).all()

        # Organize assessments by type
        user_assessments = {}
        skills_scores = {
            'technical': 0,
            'creative': 0,
            'interpersonal': 0
        }

        for assessment in assessments:
            user_assessments[assessment.assessment_type] = {
                'completed': assessment.completed,
                'score': assessment.score or 0,  # Default to 0 if None
                'created_at': assessment.created_at
            }
            if assessment.completed and assessment.score is not None:
                skills_scores[assessment.assessment_type] = assessment.score

        # Get top career matches
        career_matches = CareerPath.query.order_by(CareerPath.match_score.desc()).limit(4).all()

        logger.debug(f"User assessments: {user_assessments}")
        logger.debug(f"Skills scores: {skills_scores}")
        logger.debug(f"Career matches: {len(career_matches)} found")

        return render_template('profile.html',
                            user_assessments=user_assessments,
                            skills_scores=skills_scores,
                            career_matches=career_matches)
    except Exception as e:
        logger.error(f"Error in profile route: {str(e)}")
        flash('An error occurred while loading your profile')
        return redirect(url_for('main.index'))

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
    try:
        data = request.get_json()
        logger.debug(f"Received assessment data: {data}")

        assessment = Assessment(
            user_id=current_user.id,
            assessment_type=data['type'],
            answers=data['answers'],
            score=float(data['score']),  # Ensure score is a float
            completed=True
        )

        db.session.add(assessment)
        db.session.commit()

        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error submitting assessment: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main.route('/recommendations')
@login_required
def recommendations():
    try:
        # Get completed assessments
        assessments = Assessment.query.filter_by(
            user_id=current_user.id,
            completed=True
        ).all()

        # Calculate scores for each type
        assessment_scores = {
            'technical': 0,
            'creative': 0,
            'interpersonal': 0
        }

        for assessment in assessments:
            if assessment.score is not None:
                assessment_scores[assessment.assessment_type] = assessment.score

        logger.debug(f"Assessment scores: {assessment_scores}")

        # Get career recommendations based on assessment scores
        careers = CareerPath.query.all()
        logger.debug(f"Found {len(careers)} career paths")

        return render_template('recommendations.html',
                            technical_score=assessment_scores['technical'],
                            creative_score=assessment_scores['creative'],
                            interpersonal_score=assessment_scores['interpersonal'],
                            careers=careers)
    except Exception as e:
        logger.error(f"Error in recommendations route: {str(e)}")
        flash('An error occurred while loading recommendations')
        return redirect(url_for('main.index'))

@main.route('/apply/<int:career_id>', methods=['GET', 'POST'])
@login_required
def apply_job(career_id):
    try:
        career = CareerPath.query.get_or_404(career_id)

        if request.method == 'POST':
            application = JobApplication(
                user_id=current_user.id,
                career_path_id=career_id,
                cover_letter=request.form.get('cover_letter'),
                notes=request.form.get('notes')
            )

            db.session.add(application)
            db.session.commit()

            flash('Your application has been submitted successfully!')
            return redirect(url_for('main.recommendations'))

        return render_template('apply.html', career=career)
    except Exception as e:
        logger.error(f"Error in apply_job route: {str(e)}")
        flash('An error occurred while processing your application')
        return redirect(url_for('main.recommendations'))

@main.route('/resources')
@login_required
def resources():
    return render_template('resources.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            # Here you would typically handle the form submission
            # For now, we'll just show a success message
            flash('Thank you for your message. We will get back to you soon!')
            return redirect(url_for('main.contact'))

        return render_template('contact.html')
    except Exception as e:
        logger.error(f"Error in contact route: {str(e)}")
        flash('An error occurred while processing your request')
        return redirect(url_for('main.index'))