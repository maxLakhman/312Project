import hashlib
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection

from flask_login import login_required, current_user
from bson.objectid import ObjectId


# Connecting to MongoDB
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]

# Making collections
chat_collection = db["chat"]
post_collection = db["posts"]


chat_blueprint = Blueprint(
    "chat_blueprint",
    __name__,
    template_folder="templates"
)


@chat_blueprint.route("/chat-messages", methods=["POST"])
def chat_post():
    """Handles POST requests to /chat-messages."""
    received_data = request.get_json()

    # Checking auth token
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(
            browser_token.encode()
            ).hexdigest()

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


@chat_blueprint.route("/posts", methods=["POST"])
def post_create():
    """Handles POST requests to /posts."""
    received_data = request.get_json()

    # Checking auth token
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(
            browser_token.encode()
            ).hexdigest()

        # Finding user with same auth token
        user = user_collection.find_one(
            {"auth_token": hashed_browser_token}, {"_id": 0}
        )
        if user:
            received_data["username"] = user.get("username")
        else:
            return jsonify({"error": "Invalid auth token"}), 401

    post_collection.insert_one(received_data)

    return jsonify({"message": "Post created"}), 201


@chat_blueprint.route('/posts', methods=['GET'])
@login_required
def get_posts():
    posts = list(post_collection.find())
    for post in posts:
        post['_id'] = str(post['_id'])  # Convert ObjectId to string
    return jsonify(posts=posts), 200


@chat_blueprint.route('/posts/<string:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = post_collection.find_one({'_id': ObjectId(post_id)})
    if post is None:
        return jsonify(error='Post not found'), 404
    post_collection.update_one(
        {'_id': ObjectId(post_id)},
        {'$addToSet': {'likes': current_user.username}})

    post = post_collection.find_one({'_id': ObjectId(post_id)})
    return jsonify(likes=len(post.get('likes', []))), 200
