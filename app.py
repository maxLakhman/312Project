from flask import Flask, render_template, request, jsonify
# from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__)
# # flask_pymongo. We can use or not idc
# # Connecting MongoDB Flask
# app.config["MONGO_URI"] = "mongodb://localhost:27017/BlackJack"
# mongo = PyMongo(app)

# Connecting to MongoDB
mongo_client = MongoClient('mongo')
db = mongo_client["BlackJack"]

user_table = db["user"]
password_table = db["password"]
chat_table = db["chat"]



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

# ToDo: Register
@app.route('/register', methods=['POST'])
def register():


    received_data = request.get_json()
    username = received_data.get('username')
    password = received_data.get("password")
    password_confirm = received_data.get("password_confirm")
    print("Received username:", username)
    print("Received password:", password)
    print("Received password_confirm:", password_confirm)

    


    response_data = {"status": "success", "message": "Registration successful"}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
