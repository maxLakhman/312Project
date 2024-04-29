from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room
from app import socketio
from pymongo import MongoClient
from bson.json_util import dumps
from routes.auth import user_collection
import hashlib
from flask_login import current_user
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
@table_blueprint.route("/create-table", methods=["POST", "GET"])
def create_table():

    # checking auth token
    user = db_verify_auth_token(request)
    if not user:
        return jsonify({"status": "error", "message": "You are not logged in."})

    # create a new table
    table = {
        "table_id": str(table_collection.count_documents({}) + 1),
        "players": [],
        "deck": ["2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH",
                 "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
                 "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
                 "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
                 "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH",
                 "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
                 "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
                 "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
                 "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH",
                 "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
                 "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
                 "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
                 "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH",
                 "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
                 "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
                 "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS"],
        "dealer_hand": [], 
        "started": False,
        "game_over": False,
        "player_ready": False
    }

    # insert the table into the collection
    table_collection.insert_one(table)

    # redirect to the table
    join_table_url = url_for("table_blueprint.join_table", table_id=table.get("table_id"))

    return jsonify({"status": "success", "redirect": join_table_url})

@table_blueprint.route("/join-table/<table_id>", methods=["GET"])
def join_table(table_id):


    user = db_verify_auth_token(request)

    if not user:
        return jsonify({"status": "error", "message": "You are not logged in."})

    username = user.get("username")


    table = table_collection.find_one({"table_id": table_id})
    if not table:
        return jsonify({"status": "error", "message": "Table not found."})
    
    if table["started"] == True:
        return jsonify({"status": "error", "message": "Game has already started"})

    # check if the user is already in the table
    if username in table.get("players"):
        return render_template("table.html", table=table)
    
    # make the max players 5
    if len(table.get("players")) >= 5:
        return jsonify({"status": "error", "message": "Table is full."})

    table_collection.update_one(
        {"table_id": table_id},
        {"$push": {"players": username}}
    )

    table = table_collection.find_one({"table_id": table_id})

    # add the user's table to the user
    user_collection.update_one(
        {"username": username},
        {"$set": {"table": table_id}}
    )   
    
    return render_template("table.html", table=table)

@table_blueprint.route("/leave-table/<table_id>", methods=["GET"])
def leave_table(table_id):
    user = db_verify_auth_token(request)

    if not user:
        return jsonify({"status": "error", "message": "You are not logged in."})

    username = user.get("username")

    table = table_collection.find_one({"table_id": table_id})
    if not table:
        return jsonify({"status": "error", "message": "Table not found."})

    if username not in table.get("players"):
        return jsonify({"status": "error", "message": "You are not in this table."})

    table_collection.update_one(
        {"table_id": table_id},
        {"$pull": {"players": username}}
    )

    return redirect(url_for("lobby_blueprint.get_tables"))

