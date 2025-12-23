import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

# Use a model appropriate for chat - Gemini Pro is standard for text
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        language = data.get('language', 'en') # 'en' or 'ta'

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Create a prompt that encourages the AI to reply in the correct language
        # and be helpful and concise.
        if language == 'ta':
            system_prompt = "You are a helpful AI assistant. Reply in Tamil."
        else:
            system_prompt = "You are a helpful AI assistant. Reply in English."
            
        chat = model.start_chat(history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Okay, I will help you."]} # Prime the model
        ])
        
        response = chat.send_message(user_message)
        
        return jsonify({'response': response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
