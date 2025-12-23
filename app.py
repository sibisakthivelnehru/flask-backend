from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ CORS – browser access allow
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend running ✅"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)

        user_message = data.get("message", "")
        language = data.get("language", "en")

        if not user_message:
            return jsonify({"response": "Message empty"}), 400

        # ✅ TEMP RESPONSE (Gemini later)
        reply = f"You said: {user_message}"

        return jsonify({
            "response": reply,
            "language": language
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ["PORT"])  # Render gives this
    app.run(host="0.0.0.0", port=port)


