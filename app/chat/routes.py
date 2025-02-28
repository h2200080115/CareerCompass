from flask import jsonify, request, render_template
from flask_login import login_required
from . import chat
import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@chat.route('/chatbot')
@login_required
def chat_route():
    return render_template('chat.html')

@chat.route('/chat', methods=['POST'])
@login_required
def process_message():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({
            'status': 'error',
            'message': 'No message provided'
        }), 400

    try:
        # Check if API key is configured
        if not os.environ.get('OPENAI_API_KEY'):
            return jsonify({
                'status': 'error',
                'message': 'OpenAI API key not configured'
            }), 500

        response = client.chat.completions.create(
            model="gpt-4o",  # Latest model as of May 2024
            messages=[
                {
                    "role": "system",
                    "content": """You are a career advisor helping users with their career related questions. 
                    Provide specific, actionable advice based on the user's questions. Focus on:
                    1. Career path recommendations
                    2. Skill development suggestions
                    3. Industry insights
                    4. Job search strategies
                    5. Professional development tips"""
                },
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({
            'status': 'success',
            'response': response.choices[0].message.content
        })

    except Exception as e:
        logger.error(f"Error in chat route: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to get response from AI assistant. Please try again later.'
        }), 500