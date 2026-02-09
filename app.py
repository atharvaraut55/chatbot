from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime
from response import get_bot_response, get_bot_response_new
from flask_cors import CORS


app = Flask(__name__)
# # MongoDB connection
# client = MongoClient("mongodb://mongo:GpvYjsnClfoJmzMDbfVGKQpDHxIcsGrN@ballast.proxy.rlwy.net:41954")
# # Database connection
# db = client["chatbot_db"]
# # Chats store collection
# chats = db["chats"]
# # Answers collection
# answers = db["answers"]

client = MongoClient(os.environ.get("MONGO_URI"), serverSelectionTimeoutMS=5000)

try:
    client.server_info()
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)

db = client[os.environ.get("CHAT_DATABASE", "chatbot_db")]
chats = db[os.environ.get("CHAT_COLLECTION", "chats")]
answers = db[os.environ.get("ANS_CHAT_COLLECTION", "answers")]


#---------------------------------------------------------------
#  Bot response function
#---------------------------------------------------------------

# def get_bot_response(user_input):
#     lower_user_input = user_input.strip().lower()
#     # keywords = []

#     # 1) Fetch all keywords from MongoDB
#     keywords = answers.distinct("keywords")   # list like ["hi","rpf","rusa","fees"]
#     print(keywords)

#     if not keywords:
#         return "No keywords found in database."

#     # 2) Fuzzy match user input with keywords
#     best_match = process.extractOne(
#         lower_user_input,
#         keywords,
#         scorer=fuzz.ratio
#     )
#     print(best_match)

#     if not best_match:
#         return "No keywords found in database."

#     match_keyword, score, _ = best_match

#     # 3) Check score threshold (adjust if needed)
#     if score >= 60:   # 60-80 range
#         result = answers.find_one(
#             {"keyword": match_keyword},
#             {"ans": 1, "_id": 0}
#         )
#         if result:
#             return result["ans"]

#     return "Sorry, I didn't understand. Please type again."



# CORS(app, resources={r"/chat": {"origins": "*"}})
CORS(app, resources={r"/chat": {"origins": "http://localhost/wordpress/wordpress/"}})



#---------------------------------------------------------------
#  Root route
#--------------------------------------------------------------- 
@app.route('/')
def index():
    return render_template("index.html")



#---------------------------------------------------------------
#  chat route
#--------------------------------------------------------------- 
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message']
    bot_response = get_bot_response(user_msg)  # Define this function
    chat_doc = {"user": user_msg, "bot": bot_response, "timestamp": datetime.utcnow()}
    chats.insert_one(chat_doc)
    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


