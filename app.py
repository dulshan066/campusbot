from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Load FAQ data
try:
    with open("faq.json", "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except Exception as e:
    print(f"Error loading faq.json: {e}")
    faq_data = {}

def get_response(user_input):
    """
    Get bot response and buttons based on user input.
    Uses keywords matching and returns random response for variety.
    """
    user_input = user_input.lower()
    for intent, data in faq_data.items():
        for keyword in data.get("keywords", []):
            if keyword in user_input:
                # Get random response
                response_list = data.get("responses", [])
                response = random.choice(response_list) if response_list else "Sorry, no response found."
                # Get buttons
                buttons = data.get("buttons", [])
                return response, buttons
    # Default response if no keyword matched
    return "❓ Sorry, I didn’t understand that. Try asking about courses, timetable, lecturers, or library.", []

@app.route("/")
def index():
    """Render the chatbot UI"""
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    """Return chatbot response and buttons as JSON"""
    user_message = request.json.get("message", "")
    response, buttons = get_response(user_message)
    return jsonify({"response": response, "buttons": buttons})

if __name__ == "__main__":
    app.run(debug=True)
