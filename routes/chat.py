import json, bcrypt
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient
from bson.json_util import dumps, loads 

# Connecting to MongoDB
mongo_client = MongoClient('db')
db = mongo_client["BlackJack"]

# Making collections
chat_collection = db["chat"]

chat_blueprint = Blueprint('chat_blueprint', __name__, template_folder='templates')
@chat_blueprint.route('/chat-messages', methods=['POST'])
def chatPost():
    received_data = request.get_json()
    print(f"recieved data: {received_data}")
    chat_collection.insert_one(received_data)

    print(chat_collection.find({}))

    list_cur = list(chat_collection.find({})) 
  
    # Converting to the JSON 
    json_data = dumps(list_cur, indent = 2)  
    print(json_data)

    return jsonify(json_data)

@chat_blueprint.route('/chat-messages', methods=['GET'])
def chat_get():
    chat_box = request.args.get('chat_box')
    print(f"received data: {chat_box}")

    list_cur = list(chat_collection.find({"chat_box": chat_box})) 
  
    # Converting to the JSON 
    json_data = dumps(list_cur, indent=2)  
    print(json_data)

    return jsonify(json_data)
