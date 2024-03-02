import json, bcrypt
from flask import Flask, render_template, request, jsonify
# from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__)
# # flask_pymongo. We can use or not idc
# # Connecting MongoDB Flask
# app.config["MONGO_URI"] = "mongodb://localhost:27017/BlackJack"
# mongo = PyMongo(app)

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


# index page
@app.route('/')
def home():
    return render_template('index.html')

# setting nosniff header
@app.after_request
def set_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# auth routing framework
@app.route('/auth')
def auth():
    # parse the login info from the request here
    
    return


@app.route('/register', methods=['POST'])
def register():
    # Getting JSON request and filling variables
    received_data = request.get_json()
    username = str(received_data.get('username'))
    password = str(received_data.get("password"))
    password_confirm = str(received_data.get("password_confirm"))

    # HTML escape characters
    username = username.replace('&', '&amp;')
    username = username.replace('<', '&lt;')
    username = username.replace('>', '&gt;')

    # Checking if there will be duplicate username
    user_cursor = user_collection.find({"username": username})
    user_list = list(user_cursor)
    
    print("User_list", user_list)
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

if __name__ == '__main__':
    app.run(debug=True, port=8080)
