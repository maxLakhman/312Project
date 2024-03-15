from pymongo import MongoClient
from flask import Flask, request
import secrets, hashlib, bcrypt

# Connecting to MongoDB
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]

# Collections
user_collection = db["user"]
chat_collection = db["chat"]


# Adds message to database
def db_add_message(received_data):
    chat_collection.insert_one(received_data)


#
# Getting from DB -----------------------------------------------
#
# Returns user given username
def db_find_by_username(username):
    user_cursor = user_collection.find({"username": username})
    user_list = list(user_cursor)
    return user_list


#
# Auth Token ---------------------------------------------------
#
# Updates user database with hashed version & returns unhashed
def db_update_auth_token(username):
    auth_token = secrets.token_urlsafe(256)
    token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
    user_collection.update_one(
        {"username": username}, {"$set": {"auth_token": token_hash}}
    )

    return auth_token


def db_verify_auth_token(request):
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(browser_token.encode()).hexdigest()

        user = user_collection.find_one(
            {"auth_token": hashed_browser_token}, {"_id": 0}
        )
        return user
    return False


#
# Registration --------------------------------------------------
#
# Registers user given username
def db_register_user(username):
    salt = bcrypt.gensalt()
    password = password.encode()
    password_hash = bcrypt.hashpw(password, salt)
    record = {
        "username": username,
        "hash": password_hash,
        "salt": salt,
        "tokens": 500,
    }
    user_collection.insert_one(record)
