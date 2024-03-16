import hashlib
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection

# Connecting to MongoDB
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]

# Making collections
chat_collection = db["chat"]

chat_blueprint = Blueprint("chat_blueprint", __name__, template_folder="templates")


@chat_blueprint.route("/chat-messages", methods=["POST"])
def chat_post():
    """Handles POST requests to /chat-messages."""
    received_data = request.get_json()

    # Checking auth token
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(browser_token.encode()).hexdigest()

        # Finding user with same auth token
        user = user_collection.find_one(
            {"auth_token": hashed_browser_token}, {"_id": 0}
        )
        if user:
            received_data["username"] = user.get("username")

    chat_collection.insert_one(received_data)

    list_cur = list(chat_collection.find({}))

    # Converting to the JSON
    json_data = dumps(list_cur, indent=2)

    return jsonify(json_data)


@chat_blueprint.route("/chat-messages", methods=["GET"])
def chat_get():
    """Handles GET requests to /chat-messages."""
    chat_box = request.args.get("chat_box")

    list_cur = list(chat_collection.find({"chat_box": chat_box}))

    # Converting to the JSON
    json_data = dumps(list_cur, indent=2)

    return jsonify(json_data)
