import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai

# Load env vars
load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

# Gemini client
client = genai.Client(api_key=API_KEY)

# ✅ Health check
@app.route("/")
def home():
    return "Backend is running 🚀", 200

# ✅ Chat API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message required"}), 400

    user_message = data["message"]

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message
        )
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Render requirement
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
