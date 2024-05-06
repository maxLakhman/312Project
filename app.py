from flask import Flask, render_template, request, make_response
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS
import time

from routes.auth import *
import json

from bson.json_util import dumps
from routes.auth import user_collection

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "secret_key"
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024
socketio = SocketIO(app, cors_allowed_origins="*")

from routes import table_socket

login_manager = LoginManager()
login_manager.init_app(app)

from routes.auth import auth_blueprint, load_user
from routes.chat import chat_blueprint, chat_collection
from routes.lobby import lobby_blueprint
from routes.table import table_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(chat_blueprint)
app.register_blueprint(lobby_blueprint)
app.register_blueprint(table_blueprint)

# # # Websocket Connections
# @socketio.on("connect")
# def handle_connect():



# DDOS defense
request_counts = {}
blocked_ips = {}

def is_ip_blocked(ip):
    if ip in blocked_ips and time.time() < blocked_ips[ip]:
        return True
    return False

def add_request(ip):
    current_time = time.time()
    window_start = current_time - 10

    if ip not in request_counts:
        request_counts[ip] = []

    request_counts[ip] = [t for t in request_counts[ip] if t > window_start]

    request_counts[ip].append(current_time)

    if len(request_counts[ip]) > 50:
        blocked_ips[ip] = current_time + 30

@app.before_request
def check_rate_limit():
    ip = request.remote_addr

    if is_ip_blocked(ip):
        return make_response("Too Many Requests", 429)

    add_request(ip)


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
