from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection
import hashlib


# connecting to the MongoDB
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]

# making the collection
table_collection = db["tables"]

# blueprint for a new table
table_blueprint = Blueprint(
    "table_blueprint",
    __name__,
    template_folder="templates"
)

# route for creating a new table
@table_blueprint.route("/create-table", methods=["POST"])
def create_table():

    # checking auth token
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(
            browser_token.encode()
        ).hexdigest()

        # finding user with the same auth token
        user = user_collection.find_one({"auth_token": hashed_browser_token}, {"_id": 0})

        

    

    return jsonify(json_data)
