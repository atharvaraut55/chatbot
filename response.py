from pymongo import MongoClient
from rapidfuzz import process, fuzz
import os


# Setup connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client['chatbot_db']
# collection = db['answers']

# --------------------------------------------------------
#   MongoDb Connection
# --------------------------------------------------------
client = MongoClient(os.environ.get("MONGO_URI"), serverSelectionTimeoutMS=5000)

try:
    client.server_info()
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)

db = client[os.environ.get("CHAT_DATABASE", "chatbot_db")]
chats = db[os.environ.get("CHAT_COLLECTION", "chats")]
answers = db[os.environ.get("ANS_CHAT_COLLECTION", "answers")]



    
# --------------------------------------------------------
#   Old version
# --------------------------------------------------------
def get_bot_response(user_input):
    lower_user_input = user_input.strip().lower()

    # 1) Fetch all keywords from MongoDB
    keywords = collection.distinct("keywords")   # list like ["hi","rpf","rusa","fees"]

    if not keywords:
        return "No keywords found in database."

    # 2) Fuzzy match user input with keywords
    best_match = process.extractOne(
        lower_user_input,
        keywords,
        scorer=fuzz.ratio
    )

    if not best_match:
        return "No keywords found in database."

    match_keyword, score, _ = best_match

    # 3) Check score threshold (adjust if needed)
    if score >= 60:   # 60-80 range
        result = collection.find_one(
            {"keywords": match_keyword},
            {"answer": 1, "_id": 0}
        )
        if result:
            return result["answer"]

    return "Sorry, I didn't understand. Please type again."
    

#---------------------------------------------------------
#   New Version
#---------------------------------------------------------
def get_bot_response_new(user_input):
    user_input = user_input.strip().lower()

    best_match_score = 0
    best_answer = None

    # Fetch all documents
    docs = collection.find({})

    for doc in docs:
        keywords = doc.get("keywords", [])
        answer = doc.get("answer")

        for keyword in keywords:
            score = fuzz.ratio(user_input, keyword.lower())

            if score > best_match_score:
                best_match_score = score
                best_answer = answer

    # Adjust threshold here
    if best_match_score >= 65:
        return best_answer

    return "Sorry, I didn't understand. Please try again."
