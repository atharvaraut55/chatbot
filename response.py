from pymongo import MongoClient
from rapidfuzz import process, fuzz

# 1. Setup connection
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]
collection = db["answers"]

# 2. Global Cache (Fetch keywords once when app starts)
# This prevents high latency as your user base grows.
# cached_keywords = collection.distinct("keyword")

def get_bot_response(user_input):
    lower_user_input = user_input.strip().lower()

    # 1) Fetch all keywords from MongoDB
    keywords = collection.distinct("keyword")  # list like ["hi","rpf","rusa","fees"]

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
    if score >= 60:  # 60-80 range
        result = collection.find_one(
            {"keyword": match_keyword},
            {"ans": 1, "_id": 0}
        )
        if result:
            return result["ans"]

    return "Sorry, I didn't understand. Please type again."