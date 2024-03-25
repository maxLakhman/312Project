import hashlib
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId
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

@chat_blueprint.route("/like-message", methods=["POST"])
def like_message():
    received_data = request.get_json()

    # Checking auth token and replacing username if found
    user = db_verify_auth_token(request)
    if user:
        received_data["username"] = user.get("username")
        message_id = received_data["id"]

        chat_message = chat_collection.find_one({"_id": ObjectId(message_id)})

        # Getting list of people who liked it. Empty list if not found.
        liked_list = chat_message.get("liked_list", [])

        # If user already liked the post
        if user.get("username") in liked_list:
            response = jsonify({"success": "false"})

        # Add username to post likes
        else:
            liked_list.append(user.get("username"))
            print(liked_list)

            chat_collection.update_one(
                {"_id": ObjectId(message_id)}, {"$set": {"liked_list": liked_list}}
            )

            print()

            response = jsonify({"success": "true"})

        return response

    else:
        response = jsonify({"success": "false"})
        response.status_code = 404
        return response
    
def db_verify_auth_token(request):
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(browser_token.encode()).hexdigest()

        user = user_collection.find_one(
            {"auth_token": hashed_browser_token}, {"_id": 0}
        )
        return user
    return False
