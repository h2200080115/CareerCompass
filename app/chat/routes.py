from flask import jsonify, request, render_template
from flask_login import login_required
from . import chat
import logging
import random

logger = logging.getLogger(__name__)

# Predefined Q&A pairs for AI career guidance
qa_pairs = {
    "What career paths are available in AI?": "There are many career paths in AI including: Machine Learning Engineer, Data Scientist, AI Research Scientist, AI Ethics Specialist, Robotics Engineer, NLP Engineer, and Computer Vision Engineer. Some follow-up questions you might ask: What skills do I need for an AI career? Which AI career pays the most? How do I transition into AI from another field?",
    
    "What skills do I need for an AI career?": "Key skills for an AI career include: Programming (Python, R), mathematics (linear algebra, calculus, statistics), machine learning algorithms, deep learning frameworks (TensorFlow, PyTorch), data processing, and domain expertise. For many roles, soft skills like communication and problem-solving are also important. You might want to ask: What education is required for AI jobs? Which AI specialization is most in demand?",
    
    "Which AI career pays the most?": "Generally, AI Research Scientists, Machine Learning Engineers, and AI Architects tend to have the highest salaries in the field. Compensation also varies by location, company size, and experience level. In major tech hubs, senior AI roles can command salaries well above $150,000. Other questions you might ask: What companies hire AI professionals? How competitive is the AI job market?",
    
    "How do I transition into AI from another field?": "To transition into AI: 1) Learn fundamental AI/ML skills through online courses or bootcamps, 2) Work on personal projects to build a portfolio, 3) Network with AI professionals, 4) Apply for transitional roles that combine your existing expertise with AI, 5) Consider further education if necessary. You might want to ask: What entry-level AI jobs are available? Are AI bootcamps worth it?",
    
    "What education is required for AI jobs?": "While many AI roles prefer candidates with advanced degrees (Masters or PhD), it's increasingly possible to enter the field with a Bachelor's degree plus relevant skills and projects. Self-study through online courses and bootcamps can also be viable paths, especially when combined with a strong portfolio. You might want to ask: What are the best AI degree programs? Can I get an AI job without a degree?",
    
    "Which AI specialization is most in demand?": "Currently, Machine Learning Engineers, NLP Specialists, and AI Application Developers are in high demand. Emerging areas like AI Ethics and Explainable AI are also growing rapidly. The most in-demand skills include deep learning, natural language processing, and computer vision. You might want to ask: What is the future outlook for AI jobs? Which industries hire the most AI professionals?",
    
    "What companies hire AI professionals?": "AI professionals are hired by: 1) Tech giants (Google, Microsoft, Amazon, Meta), 2) Specialized AI companies (OpenAI, Anthropic, DeepMind), 3) Financial institutions, 4) Healthcare organizations, 5) Manufacturing companies, 6) Startups across various sectors, and 7) Government and research institutions. You might want to ask: How do I prepare for AI job interviews? What's the work environment like in AI jobs?",
    
    "What is the future outlook for AI jobs?": "The outlook for AI jobs is extremely positive with continued growth expected for the next decade. As AI becomes integrated into more industries, demand for skilled professionals will likely increase. Emerging areas like generative AI, AI ethics, and AI safety are creating new specializations. You might want to ask: Will AI replace jobs or create more? How can I stay relevant in the AI field?",
    
    "How do I prepare for AI job interviews?": "To prepare for AI interviews: 1) Study machine learning fundamentals, 2) Practice coding problems and algorithms, 3) Be ready to explain your projects in detail, 4) Prepare for system design questions, 5) Review statistics and probability, 6) Be prepared to discuss real-world applications, and 7) Research the company's AI initiatives. You might want to ask: What are common AI interview questions? How do I create an AI portfolio?",
    
    "hlo":"how are you"
}

# Default response if no match is found
default_response = "I don't have information on that specific topic yet. I can answer questions about AI careers, skills needed, education requirements, and job prospects. You could try asking: What career paths are available in AI? What skills do I need for an AI career? How do I transition into AI from another field?"

@chat.route('/chatbot')
@login_required
def chat_route():
    return render_template('chat.html')

@chat.route('/chat', methods=['POST'])
@login_required
def process_message():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'message': 'No message provided'
            }), 400
        
        # Look for exact match first
        response = qa_pairs.get(user_message)
        
        # If no exact match, look for keywords
        if not response:
            for question, answer in qa_pairs.items():
                # Simple keyword matching (could be improved with NLP)
                keywords = set(question.lower().split()) - {'is', 'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or'}
                user_keywords = set(user_message.lower().split()) - {'is', 'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or'}
                
                # If there's significant keyword overlap, use this answer
                if len(keywords.intersection(user_keywords)) >= 2:
                    response = answer
                    break
        
        # Use default response if still no match
        if not response:
            response = default_response
            
        return jsonify({
            'status': 'success',
            'response': response
        })
        
    except Exception as e:
        logger.error(f"Error in chat route: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to process your question. Please try again later.'
        }), 500