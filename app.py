from flask import Flask, render_template, request, jsonify
import json
import random
import os

app = Flask(__name__)

# Load FAQ data
try:
    with open("faq.json", "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except Exception as e:
    print(f"Error loading faq.json: {e}")
    faq_data = {}

def get_response(user_input):
    user_input = user_input.lower()
    for intent, data in faq_data.items():
        for keyword in data.get("keywords", []):
            if keyword in user_input:
                response_list = data.get("responses", [])
                response = random.choice(response_list) if response_list else "Sorry, no response found."
                buttons = data.get("buttons", [])
                return response, buttons
    return "❓ Sorry, I didn’t understand that. Try asking about courses, timetable, lecturers, or library.", []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_message = request.json.get("message", "")
    response, buttons = get_response(user_message)
    return jsonify({"response": response, "buttons": buttons})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
