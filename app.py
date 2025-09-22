import os
import json
import time
import uuid
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required but not found")

genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

class ChatManager:
    def __init__(self):
        self.sessions = {}
    
    def get_or_create_session(self, session_id):
        """Get or create a chat session for a user"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'chat': model.start_chat(),
                'history': []
            }
        return self.sessions[session_id]
    
    def generate_response(self, session_id, user_message):
        """Generate response using Gemini API with proper session management"""
        try:
            chat_session = self.get_or_create_session(session_id)
            chat = chat_session['chat']
            
            # Send message to the chat session (maintains context automatically)
            response = chat.send_message(user_message)
            
            if not response or not response.text:
                return "Sorry, I couldn't generate a response at the moment."
            
            bot_response = response.text
            
            # Update conversation history for this session
            chat_session['history'].extend([
                {"role": "user", "message": user_message},
                {"role": "assistant", "message": bot_response}
            ])
            
            return bot_response
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while processing your request. Please try again."
    
    def clear_session(self, session_id):
        """Clear conversation history for a specific session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
        return "Conversation history cleared."
    
    def get_session_history(self, session_id):
        """Get conversation history for a session"""
        if session_id in self.sessions:
            return self.sessions[session_id]['history']
        return []

# Initialize chat manager
chat_manager = ChatManager()


def get_session_id():
    """Get or create a session ID for the user"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']


@app.route('/')
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        if len(user_message) > 10000:  # Input length check
            return jsonify({
                'success': False,
                'error': 'Message too long. Please keep it under 10,000 characters.'
            }), 400
        
        session_id = get_session_id()
        
        # Generate response using the chat manager
        response = chat_manager.generate_response(session_id, user_message)
        
        return jsonify({
            'success': True,
            'response': response,
            'message': user_message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    try:
        session_id = get_session_id()
        message = chat_manager.clear_session(session_id)
        return jsonify({
            'success': True,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Gemini Flask Bot is running',
        'timestamp': str(int(time.time()))
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for external integrations"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        if len(user_message) > 10000:  # Input length check
            return jsonify({
                'success': False,
                'error': 'Message too long. Please keep it under 10,000 characters.'
            }), 400
        
        # For API endpoint, use a session ID from header or create a temporary one
        session_id = request.headers.get('X-Session-ID', str(uuid.uuid4()))
        
        response = chat_manager.generate_response(session_id, user_message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': str(int(time.time())),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history for the current session"""
    try:
        session_id = get_session_id()
        history = chat_manager.get_session_history(session_id)
        return jsonify({
            'success': True,
            'history': history,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

if __name__ == '__main__':
    print("🤖 Starting Gemini Flask Bot...")
    print(f"📝 Web interface will be available at: http://localhost:5000")
    print(f"🔗 API endpoint: http://localhost:5000/api/chat")
    print(f"✅ Gemini API key loaded successfully")
    
    app.run(host='0.0.0.0', port=5000, debug=True)