import json, bcrypt
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates')

# Connecting to MongoDB
mongo_client = MongoClient('db')
db = mongo_client["BlackJack"]

# Making collections
user_collection = db["user"]
chat_collection = db["chat"]
chat_id_collection = db["chat_id"]

 # Setting default chat id
if chat_id_collection.count_documents({}) == 0:
    chat_id_collection.insert_one({"_id" : 1, "message_id" : 1})

# auth routing framework
@auth_blueprint.route('/auth', methods=['POST'])
def auth():
    # Getting JSON request and filling variables
    received_data = request.get_json()
    username = received_data.get('username')
    password = received_data.get('password')

    # HTML escape characters
    username = username.replace('&', '&amp;')
    username = username.replace('<', '&lt;')
    username = username.replace('>', '&gt;')

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
            response_data = {"status": "success", "message": "Welcome " + username}
        else:
            response_data = {"status": "error", "message": "Invalid Credentials"}


    return jsonify(response_data)



@auth_blueprint.route('/register', methods=['POST'])
def register():
    # Getting JSON request and filling variables
    received_data = request.get_json()
    username = received_data.get('username')
    password = received_data.get("password")
    password_confirm = received_data.get("password_confirm")

    # HTML escape characters
    username = username.replace('&', '&amp;')
    username = username.replace('<', '&lt;')
    username = username.replace('>', '&gt;')

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
        record = {"username": username, "hash": password_hash, "salt": salt}
        user_collection.insert_one(record)

        response_data = {"status": "success", "message": "Registration Successful"}
       

    return jsonify(response_data)