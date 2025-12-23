import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    language = data.get("language", "en")

    if not message:
        return jsonify({"error": "No message"}), 400

    if language == "ta":
        prompt = "Reply in Tamil: " + message
    else:
        prompt = "Reply in English: " + message

    response = model.generate_content(prompt)
    return jsonify({"response": response.text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



