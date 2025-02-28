from flask import jsonify, request
from flask_login import login_required
from . import chat
import os
from openai import OpenAI
from openai import OpenAIError  # Updated import

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@chat.route('/chat', methods=['POST'])
@login_required
def get_response():
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

    except OpenAIError as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get response from AI assistant. Please try again later.'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500