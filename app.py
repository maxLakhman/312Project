from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS
from routes.auth import auth_blueprint, load_user
from routes.chat import chat_blueprint, chat_collection
from routes.lobby import lobby_blueprint
from routes.table import table_blueprint
from routes.auth import *
import json

from bson.json_util import dumps
from routes.auth import user_collection

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

from routes import table_socket

login_manager = LoginManager()
login_manager.init_app(app)


# # Websocket Connections
# @socketio.on("connect")
# def handle_connect():
#     print("Connection Successful")


# @socketio.on("disconnect")
# def handle_disconnect():
#     print("Disconnection Successful")


@socketio.on("send_message")
def handle_send_message(data):

    # Checking auth token
    print(current_user)
    if current_user.is_authenticated:
        user = user_collection.find_one(
            {"username": current_user.username}
        )
        if user:
            data["username"] = user.get("username")
            data["profile_pic"] = user.get(
                "profile_pic", "static/images/profiles/default"
            )
        else:
            data["profile_pic"] = "static/images/profiles/default"
    else:
        data['username'] = "guest"
        data["profile_pic"] = "static/images/profiles/default"

    list_cur = chat_collection.insert_one(data)
    inserted_id = list_cur.inserted_id

    inserted_document = chat_collection.find_one({"_id": inserted_id})

    # Converting to the JSON
    json_data = dumps(inserted_document, indent=2)

    emit("new_message", json_data, broadcast=True)


# Sets pfp for current_user
@login_manager.user_loader
def load_user(username):
    user_info = list(user_collection.find({"username": username}))
    if user_info:
        user = User(username)
        user.profile_pic = user_info[0].get(
            "profile_pic", "static/images/profiles/default"
        )
        return user
    return None


login_manager.user_loader(load_user)


app.register_blueprint(auth_blueprint)
app.register_blueprint(chat_blueprint)
app.register_blueprint(lobby_blueprint)
app.register_blueprint(table_blueprint)


@app.route("/")
def home():
    """Render the index page."""
    return render_template("index.html")


@app.route("/settings.html")
def open_settings():
    """Render the settings page."""
    return render_template("settings.html")


# @app.route('../static/music/Morning-Routine-Lofi-Study-Music(chosic.com).mp3')
# def serve_music():
#    return render_template("../static/music/Morning-Routine-Lofi-Study-Music(chosic.com).mp3")
@app.after_request
def set_header(response):
    """Set the 'X-Content-Type-Options' header to 'nosniff'."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


if __name__ == "__main__":
    socketio.run(app, debug=True)
