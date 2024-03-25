from flask import Blueprint, jsonify, request, redirect, url_for
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection
import hashlib
import uuid


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


def db_verify_auth_token(request):
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(browser_token.encode()).hexdigest()

        user = user_collection.find_one(
            {"auth_token": hashed_browser_token}, {"_id": 0}
        )
        return user
    return False



# route for creating a new table
@table_blueprint.route("/create-table", methods=["POST"])
def create_table():

    # checking auth token
    user = db_verify_auth_token(request)
    if not user:
        return jsonify({"status": "error", "message": "You are not logged in."})
    
    # find the username
    username = user.get("username")
    
    # table count

    # create a new table
    table = {
        "table_id": str(table_collection.count_documents({}) + 1),
        "players": [username],
        "deck": [],
        "dealer": [],
        "game_over": False
    }

    # insert the table into the collection
    table_collection.insert_one(table)

    return redirect(url_for("join_table", table_id=table.get("table_id")))

@table_blueprint.route("/join-table/<table_id>")
def join_table(table_id):
    user = db_verify_auth_token(request)

    if not user:
        return jsonify({"status": "error", "message": "You are not logged in."})

    username = user.get("username")

    table = table_collection.find_one({"table_id": table_id})
    if not table:
        return jsonify({"status": "error", "message": "Table not found."})

    # make the max players 5
    if len(table.get("players")) >= 5:
        return jsonify({"status": "error", "message": "Table is full."})

    table_collection.update_one(
        {"table_id": table_id},
        {"$push": {"players": username}}
    )

    return jsonify({"status": "success", "message": "Joined table."})