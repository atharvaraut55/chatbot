import os
from pymongo import MongoClient
 

# mongodb = "mongodb://localhost:27017/"
# client = MongoClient(os.environ.get("MONGO_URI"))
# db = client['chatbot_db']
# chats = db['answers']

os.environ["CHAT_DATABASE"] = "chatbot_db"

os.environ["CHAT_COLLECTION"] = "chats"

os.environ["ANS_CHAT_COLLECTION"] = "answers"

os.environ["MONGO_URI"] = "mongodb://localhost:27017/"

os.environ["DEBUG_MODE_FLASK"] = True

