import json, bcrypt
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient

chat_blueprint = Blueprint('chat_blueprint', __name__, template_folder='templates')
@auth_blueprint.route('/chat-messages', methods=['POST'])
def show(page):
    # stuff
    print("chat message")

    received_data = request.get_json()

    print(f"recieved data: {received_data}")