from flask import Blueprint, jsonify, make_response, redirect, request, url_for, current_app, render_template
from pymongo import MongoClient
from routes.auth import user_collection
from routes.table import table_collection
import uuid

# connecting to the MongoDB
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]

# retrieving table collection
table_collection = db["tables"]

# blueprint for the lobby
lobby_blueprint = Blueprint(
    "lobby_blueprint",
    __name__,
    template_folder="templates"
)

# generate the appropriate amount of tables in the lobby
@lobby_blueprint.route("/lobby", methods=["GET"])
def get_tables():
    tables = list(table_collection.find({}))
    return render_template("lobby.html", tables=tables)



