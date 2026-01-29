from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime
from response import get_bot_response
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.environ.get("MONGO_URI"))

# Database connection
db = client[str(os.environ.get("CHAT_DATABASE"))]

# Chats store collection
chats = db[str(os.environ.get("CHAT_COLLECTION"))]

# Answers collection
answers = db[str(os.environ.get("ANS_CHAT_COLLECTION"))]

# adding CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)

    user_msg = data.get('message')
    session_id = data.get('session_id')

    last_activity = activity.find_one(
        {"session_id": session_id},
        sort=[("timestamp", -1)]
    )

    page_context = ""
    if last_activity:
        page_context = f"User is currently on page: {last_activity.get('page_title')} ({last_activity.get('page_url')})"

    bot_response = get_bot_response(user_msg, page_context)

    chats.insert_one({
        "session_id": session_id,
        "user": user_msg,
        "bot": bot_response,
        "page": page_context,
        "timestamp": datetime.utcnow()
    })

    return jsonify({'response': bot_response})




# from flask import Flask, request, 

# New collection
activity = db["user_activity"]

@app.route('/track', methods=['POST'])
def track_user():
    data = request.json

    session_id = data.get("session_id")

    activity.insert_one({
        "session_id": session_id,
        "page_url": data.get("page_url"),
        "page_title": data.get("page_title"),
        "referrer": data.get("referrer"),
        "timestamp": datetime.utcnow()
    })

    return jsonify({"status": "tracked"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
