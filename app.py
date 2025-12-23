from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Health check
@app.route("/")
def home():
    return "Backend is running 🚀", 200

# Chat route (TEMP MOCK)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message required"}), 400

    message = data["message"]

    # TEMP RESPONSE (no Gemini)
    return jsonify({
        "response": f"You said: {message}"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
