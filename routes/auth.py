import json, bcrypt, secrets, hashlib
from flask import Flask, render_template, request, jsonify, Blueprint, make_response
from pymongo import MongoClient

auth_blueprint = Blueprint("auth_blueprint", __name__, template_folder="templates")

# Connecting to MongoDB
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]

# Making collections
user_collection = db["user"]


# auth routing framework
@auth_blueprint.route("/auth", methods=["POST"])
def auth():
    # Getting JSON request and filling variables
    received_data = request.get_json()
    username = received_data.get("username")
    password = received_data.get("password")

    # HTML escape characters
    username = username.replace("&", "&amp;")
    username = username.replace("<", "&lt;")
    username = username.replace(">", "&gt;")

    # Getting record of username
    user_cursor = user_collection.find({"username": username})
    user_list = list(user_cursor)

    # Checking if a field is empty
    if not username or not password:
        response_data = {"status": "error", "message": "Empty Field"}
    # If username not found
    elif not user_list:
        response_data = {"status": "error", "message": "Invalid Credentials"}
    # Adding salt to given pw, hashing, then comparing to known user hash
    else:
        user_password = user_list[0]["hash"]
        user_salt = user_list[0]["salt"]
        password = password.encode()

        check_pass = bcrypt.hashpw(password, user_salt)

        if check_pass == user_password:
            # Making auth token log2(64^256) = 1536 bits of entropy
            auth_token = secrets.token_urlsafe(256)
            token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
            user_collection.update_one(
                {"username": username}, {"$set": {"auth_token": token_hash}}
            )

            # Making response
            response_data = {"status": "success", "message": "Welcome " + username}
            response = make_response(jsonify(response_data))
            response.set_cookie("auth_token", auth_token)
            return response
        else:
            response_data = {"status": "error", "message": "Invalid Credentials"}

    return jsonify(response_data)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    # Getting JSON request and filling variables
    received_data = request.get_json()
    username = received_data.get("username")
    password = received_data.get("password")
    password_confirm = received_data.get("password_confirm")

    # HTML escape characters
    username = username.replace("&", "&amp;")
    username = username.replace("<", "&lt;")
    username = username.replace(">", "&gt;")

    # Checking if there will be duplicate username
    user_cursor = user_collection.find({"username": username})
    user_list = list(user_cursor)

    # Empty Field
    if not username or not password or not password_confirm:
        response_data = {"status": "error", "message": "Empty Field"}

    # Duplicate Username
    elif user_list:
        response_data = {"status": "error", "message": "Username Taken"}

    # Password Missmatch
    elif password != password_confirm:
        response_data = {"status": "error", "message": "Password Mismatch"}

    # Register User
    else:
        # Hashing & salting password
        salt = bcrypt.gensalt()
        password = password.encode()
        password_hash = bcrypt.hashpw(password, salt)

        # Making record and adding to database
        record = {
            "username": username,
            "hash": password_hash,
            "salt": salt,
            "tokens": 500,
        }
        user_collection.insert_one(record)

        response_data = {"status": "success", "message": "Registration Successful"}

    return jsonify(response_data)
