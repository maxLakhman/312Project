import json, bcrypt, hashlib
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson import ObjectId
from routes.auth import *
from routes.function_handler import *

chat_blueprint = Blueprint("chat_blueprint", __name__, template_folder="templates")


@chat_blueprint.route("/chat-messages", methods=["POST"])
def chatPost():
    received_data = request.get_json()

    # Checking auth token and replacing username if found
    user = db_verify_auth_token(request)
    if user:
        received_data["username"] = user.get("username")

    print(f"recieved data: {received_data}")
    db_add_message(received_data)

    print(chat_collection.find({}))

    list_cur = list(chat_collection.find({}))

    # Converting to the JSON
    json_data = dumps(list_cur, indent=2)
    print(json_data)

    return jsonify(json_data)


@chat_blueprint.route("/chat-messages", methods=["GET"])
def chat_get():
    chat_box = request.args.get("chat_box")
    print(f"received data: {chat_box}")

    list_cur = list(chat_collection.find({"chat_box": chat_box}))

    # Converting to the JSON
    json_data = dumps(list_cur, indent=2)
    print(json_data)

    return jsonify(json_data)

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

            chat_collection.update_one(
                {"_id": message_id}, {"$set": {"liked_list": liked_list}}
            )

            response = jsonify({"success": "true"})

        return response

    else:
        response = jsonify({"error": "Not Found"})
        response.status_code = 404
        return response