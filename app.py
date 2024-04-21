from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, join_room, leave_room, emit
from routes.auth import auth_blueprint, load_user
from routes.chat import chat_blueprint
from routes.lobby import lobby_blueprint
from routes.table import table_blueprint
from routes.auth import *

app = Flask(__name__)
app.secret_key = "super_secret_key"
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Set the user_loader function
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
    socketio.run(app, debug=True, port=8080)
